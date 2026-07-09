
from sqlmodel import Session, select

from app.src.expenses.models import ExpenseSplit, Expenses
from app.src.payments.models import Payments
from app.src.payments.services import calculate_balance


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
    statement = select(Expenses , ExpenseSplit).join(ExpenseSplit).where(Expenses.id == user_id)
    result =  session.exec(statement).all()
    splits = [split for _ , split in result]
    return splits


def get_balance(session : Session , user_id : int):
    expense_splits_to_pay = retrieve_expenses(session , user_id)
    paid_payments = retrieve_payments_paid(session , user_id)
    splits_to_get = retrieve_amount_to_get(session , user_id)

    balance = calculate_balance(
        paid=paid_payments,
        to_get=splits_to_get,
        expenses_split=expense_splits_to_pay
    )
    
    return balance



