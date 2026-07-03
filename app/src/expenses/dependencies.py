from fastapi import HTTPException, status
from sqlmodel import Session, select, func

from app.src.expenses.models import ExpenseIn, ExpenseSplit, Expenses
from app.src.expenses.services import splitter
from app.src.groups.models import UserGroupJunction


def add_expense (expense_data :ExpenseIn , session : Session , user_id : int , group_id : int) ->list[ExpenseSplit]:
    expense = Expenses(
        user_id=user_id,
        group_id=group_id,
        **expense_data.model_dump()
    )
    session.add(expense)
    session.commit()
    session.refresh(expense)

    if not expense.id :
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Expense is not created"
        )



    statement = select(UserGroupJunction.user_id).where(UserGroupJunction.group_id == group_id)
    member_ids = [row for row in session.exec(statement).all()]
    if not member_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} has no members"
        )

    expense_split = splitter(
        expense=expense_data,
        user_id=user_id,
        expense_id=expense.id,
        member_ids=member_ids,
    )

    session.add_all(expense_split)
    session.commit()
    for exp_split in expense_split:
        session.refresh(exp_split)
    

    return expense_split