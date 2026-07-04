from fastapi import APIRouter, HTTPException , status

from app.core.database import SessionDep
from app.src.auth.dependencies import CurrentUserDep
from app.src.expenses.dependencies import add_expense, list_group_expences, list_user_expences
from app.src.expenses.models import ExpenseIn, ExpenseSplit, Expenses


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

@router.get("/{group_id}" , response_model=list[Expenses])
def get_group_expense(group_id: int , session : SessionDep , user : CurrentUserDep):
    if not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is not authorized to use this endpoint"
        )
    expences = list_group_expences(
        session=session,
        user_id=user.id,
        group_id=group_id
    )

    return expences

@router.get("/" , response_model=list[Expenses])
def get_user_expences(session: SessionDep , user : CurrentUserDep):
    if not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is not authorized to use this endpoint"
        )
    
    expences = list_user_expences(
        session=session,
        user_id=user.id
    )

    return expences