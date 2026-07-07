from decimal import Decimal, ROUND_HALF_UP
from typing import Sequence

from fastapi import HTTPException

from app.src.expenses.exceptions import SplitsInputConflict, SplitsRequiredError
from app.src.expenses.models import ExpenseIn, ExpenseSplit, Split


def splitter(expense: ExpenseIn, user_id: int, expense_id: int, member_ids: Sequence[int]):
    if not member_ids:
        raise HTTPException(status_code=422, detail=f"Group must have at least one member.")

    total_amt: Decimal = expense.total_amt
    payer_id = user_id
    n = len(member_ids)
    decided_amts: list[Decimal] = [Decimal("0.00")] * n

    if expense.split_type == Split.disproportionate:
        if not expense.splits:
            raise SplitsRequiredError()
        if len(expense.splits) != n:
            raise HTTPException(status_code=422, detail=f"Number of split entries must match group members.")

        split_map = {split.user_id: split.percentage for split in expense.splits}
        if set(split_map) != set(member_ids):
            raise SplitsInputConflict()

        decided_amts = [
            (total_amt * Decimal(split_map[user_id]) / Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            for user_id in member_ids
        ]
    else:
        per = (total_amt / Decimal(n)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        decided_amts = [per for _ in range(n)]

    round_rem = total_amt - sum(decided_amts)
    decided_amts[0] = (decided_amts[0] + round_rem).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    expense_splited = [
        ExpenseSplit(user_id=user_id, expense_id=expense_id, decided_amt=amt)
        for user_id, amt in zip(member_ids, decided_amts)
        if user_id != payer_id
    ]

    return expense_splited