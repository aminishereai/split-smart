from decimal import Decimal, ROUND_HALF_UP

from app.src.expenses.models import ExpenseIn, ExpenseSplit, Split


def splitter(expense: ExpenseIn , user_id : int , expense_id : int , n : int):
    total_amt: Decimal = expense.total_amt
    decided_amts: list[Decimal] = [Decimal('0.00')] * n
    payer_id = user_id

    assert expense.splits is not None
    if expense.split_type == Split.disproportionate:
        decided_amts = [ (total_amt * Decimal(x.percentage) / Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) for x in expense.splits]
        
    if expense.split_type == Split.equal :
        per = (total_amt / Decimal(n)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        decided_amts = [per for _ in range(n)]

    round_rem = (total_amt - sum(decided_amts))
    decided_amts[0] = (decided_amts[0] + round_rem).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # create expeense split object 
    expense_splited = [ExpenseSplit(user_id = x.user_id , expense_id = expense_id , decided_amt=y) for x , y in zip(expense.splits , decided_amts)]
    
    # Filters the payer amt altogether
    expense_splited = [x for x in expense_splited if x.user_id != payer_id]

    return expense_splited