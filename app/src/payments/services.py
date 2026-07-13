from decimal import Decimal
from typing import Sequence

from app.src.expenses.models import ExpenseSplit, Expenses
from app.src.payments.models import Payments


def calculate_balance (paid : Sequence[Payments] , to_get : Sequence[ExpenseSplit] , expenses_split : Sequence[ExpenseSplit] , recived_amt : Sequence[Payments]):
    balance : Decimal | int  = Decimal(0)

    paid_balance = sum([x.payed_amt for x in paid])
    to_pay = sum([x.decided_amt for x in expenses_split])
    to_get_amt = sum([x.decided_amt for x in to_get])
    recived_paid_amt = sum([x.payed_amt for x in recived_amt])

    balance = paid_balance - to_pay + to_get_amt - recived_paid_amt

    return balance

