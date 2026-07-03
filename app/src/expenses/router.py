from fastapi import APIRouter

from app.core.database import SessionDep
from app.src.auth.dependencies import CurrentUserDep
from app.src.expenses.dependencies import add_expense
from app.src.expenses.models import ExpenseIn, ExpenseSplit


router = APIRouter(
    prefix="/expense",
    tags=["Expences"])


@router.post("/{group_id}" , response_model=list[ExpenseSplit])
def post_expense(group_id : int ,expense : ExpenseIn , session : SessionDep , user : CurrentUserDep):
    
    assert user.id is not None
    expense_splited = add_expense(
        expense_data=expense,
        session=session,
        user_id=user.id,
        group_id=group_id
    )

    return expense_splited



