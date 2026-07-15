from fastapi import APIRouter, HTTPException

from app.core.database import SessionDep
from app.src.auth.dependencies import CurrentUserDep
from app.src.payments.dependencies import add_payment, get_balance, simplify
from app.src.payments.models import Balance, Payments, PaymentsCreate, PaymentsOut, SimplifiedDebts


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

cred_exceptions = HTTPException(401 , detail=f"User Not Authorized to use this endpoint.")
 
@router.post("/" , response_model=PaymentsOut)
def post_payments(payment_in  : PaymentsCreate , session : SessionDep , user : CurrentUserDep):
    if not user.id :
        raise cred_exceptions
    

    payment = Payments(
        payer_id=user.id,
        **payment_in.model_dump()
    )

    payment = add_payment(payment , session)

    return payment


@router.get("/view" , response_model=Balance)
def view_balance(session : SessionDep , user : CurrentUserDep):
    if not user.id :
        raise cred_exceptions
    
    balance = get_balance(
        session=session,
        user_id=user.id
    )

    return Balance(balance=balance)

@router.get("/simplify" , response_model=SimplifiedDebts)
def simplify_debt(session : SessionDep , user : CurrentUserDep):
    if not user.id :
        raise cred_exceptions

    debts_simplified = simplify(
        session=session,
        user_id=user.id
    )

    return debts_simplified