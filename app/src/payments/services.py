from collections import deque
from decimal import Decimal
from typing import Sequence

from app.src.expenses.models import ExpenseSplit
from app.src.payments.models import Payments


def calculate_balance (paid : Sequence[Payments] , to_get : Sequence[ExpenseSplit] , expenses_split : Sequence[ExpenseSplit] , recived_amt : Sequence[Payments]):
    balance : Decimal | int  = Decimal(0)

    paid_balance = sum([x.payed_amt for x in paid])
    to_pay = sum([x.decided_amt for x in expenses_split])
    to_get_amt = sum([x.decided_amt for x in to_get])
    recived_paid_amt = sum([x.payed_amt for x in recived_amt])

    balance = paid_balance - to_pay + to_get_amt - recived_paid_amt

    return balance

def assign(creditors_in : list[tuple[int , Decimal | int]] , debitors_in : list[tuple[int , Decimal | int]]) -> list[tuple[int , int , Decimal|int]]:
    creditors , debitors = deque(creditors_in) , deque(debitors_in)
    transfer : list[tuple[int , int , Decimal|int]] = []
    while creditors and debitors :
        creditor ,creditor_balance = creditors.popleft()
        debitor , debitor_balance = debitors.popleft()

        settle = min(creditor_balance , debitor_balance)
        creditor_balance -= settle
        debitor_balance += settle

        transfer.append((creditor , debitor , settle))

        if creditor_balance :
            creditors.appendleft((creditor , creditor_balance))

        if debitor_balance :
            debitors.appendleft((debitor , debitor_balance))
        
    return transfer


def filter_user_transfer(user_id : int , transfer : list[tuple[int , int , Decimal|int]] , is_debitor: bool=False)-> list[tuple[int , int , Decimal|int]] :
    index = 1 if is_debitor else 0
    filtered = [transf for transf in transfer if (transf[index] == user_id) ]
    return filtered