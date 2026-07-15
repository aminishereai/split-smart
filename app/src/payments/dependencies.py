from decimal import Decimal

from sqlalchemy import func
import sqlalchemy
from sqlmodel import Session, col, select

from app.src.expenses.models import ExpenseSplit, Expenses
from app.src.groups.models import UserGroupJunction
from app.src.payments.models import Payments, SimplifiedDebts
from app.src.payments.services import assign, calculate_balance, filter_user_transfer


def add_payment(payments : Payments , session : Session):
    session.add(payments)
    session.commit()
    session.refresh(payments)

    return payments


def retrieve_expenses(session : Session , user_id : int):
    statement = select(ExpenseSplit).where(ExpenseSplit.user_id == user_id)
    return session.exec(statement).all()

def retrieve_payments_paid(session : Session , user_id : int):
    statement = select(Payments).where(Payments.payer_id == user_id)
    return session.exec(statement).all()

def retrieve_amount_to_get(session : Session , user_id : int):
    statement = select(Expenses , ExpenseSplit).join(ExpenseSplit).where(Expenses.user_id == user_id)
    result =  session.exec(statement).all()
    splits = [split for _ , split in result]
    return splits

def retrieve_recived_payments(session : Session , user_id : int):
    statement = select(Payments).where(Payments.lender_id == user_id)
    return session.exec(statement).all()



def get_balance(session : Session , user_id : int):
    expense_splits_to_pay = retrieve_expenses(session , user_id)
    paid_payments = retrieve_payments_paid(session , user_id)
    splits_to_get = retrieve_amount_to_get(session , user_id)
    recived_amt = retrieve_recived_payments(session , user_id)

    balance = calculate_balance(
        paid=paid_payments,
        to_get=splits_to_get,
        expenses_split=expense_splits_to_pay,
        recived_amt = recived_amt
    )
    
    return balance

def get_debt_info(session: Session , user_id : int):
    my_groups = (select(UserGroupJunction.group_id).where(UserGroupJunction.user_id == user_id))
    users_ids = (select(UserGroupJunction.user_id).where(col(UserGroupJunction.group_id).in_(my_groups) , UserGroupJunction.user_id != user_id))
    
    amt_owed_query = select(ExpenseSplit.user_id ,func.sum(ExpenseSplit.decided_amt).label("amount_owed")).where(col(ExpenseSplit.user_id).in_(users_ids)).group_by(col(ExpenseSplit.user_id)).subquery()


    paid_query = select(Payments.payer_id , func.sum(Payments.payed_amt).label("paid_amt")).where(
        col(Payments.payer_id).in_(users_ids),        
    ).group_by(col(Payments.payer_id)).subquery()



    recived_query = select(Payments.lender_id , func.sum(Payments.payed_amt).label("recived_amt")).where(
        col(Payments.lender_id).in_(users_ids)
    ).group_by(col(Payments.lender_id)).subquery()



    lent_query = select(Expenses.user_id , func.sum(ExpenseSplit.decided_amt)
                        .label("lended_amt")).where(col(Expenses.user_id).in_(users_ids)).join(ExpenseSplit).group_by(col(Expenses.user_id)).subquery()
    

    statement = sqlalchemy.select(
        amt_owed_query.c.user_id,
        func.coalesce(lent_query.c.lended_amt, 0).label("lended_amt"),
        func.coalesce(paid_query.c.paid_amt, 0).label("paid_amt"),
        func.coalesce(recived_query.c.recived_amt, 0).label("recived_amt"),
        func.coalesce(amt_owed_query.c.amount_owed, 0).label("amount_owed"),

    ).select_from(amt_owed_query).outerjoin(
        lent_query,
        lent_query.c.user_id == amt_owed_query.c.user_id
    ).outerjoin(
        paid_query,
        paid_query.c.payer_id == amt_owed_query.c.user_id
    ).outerjoin(
        recived_query,
        recived_query.c.lender_id == amt_owed_query.c.user_id
    )

    return session.execute(statement).all()






def simplify(session : Session , user_id : int) -> SimplifiedDebts:
    debt_infos = get_debt_info(session , user_id)
    balances = {}
    for row in debt_infos:
        net_balance = (
            (row.lended_amt or 0 )-
            (row.paid_amt or 0 )-
            (row.recived_amt or 0) +
            (row.amount_owed or 0)
        )
        balances[row.user_id] = net_balance
    
    creditors = [(x, y) for x, y in balances.items() if y > 0]
    creditors = sorted(creditors, key=lambda item: item[1], reverse=True)
    debitors = [(x, y) for x, y in balances.items() if y < 0]
    debitors = sorted(debitors, key=lambda item: item[1])

    transfer_assigned = assign(creditors , debitors)

    paying_transfer = filter_user_transfer(
        user_id=user_id,
        transfer=transfer_assigned
    )

    recieving_transfer = filter_user_transfer(
        user_id=user_id,
        transfer=transfer_assigned,
        is_debitor=True
    )

    truncate = lambda transfers : [(transfer[1:]) for transfer in transfers]

    you_owe : list[tuple[int ,Decimal]] = truncate(paying_transfer)
    owed_to_you : list[tuple[int , Decimal]] = truncate(recieving_transfer)

    return SimplifiedDebts(
        you_owe=you_owe,
        owed_to_you=owed_to_you
    )



