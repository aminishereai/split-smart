from fastapi import APIRouter, HTTPException

from app.core.database import SessionDep
from app.src.auth.dependencies import CurrentUserDep
from app.src.payments.dependencies import add_payment
from app.src.payments.models import Payments, PaymentsCreate, PaymentsOut


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.post("/" , response_model=PaymentsOut)
def post_payments(payment_in  : PaymentsCreate , session : SessionDep , user : CurrentUserDep):
    if not user.id :
        raise HTTPException(401)
    

    payment = Payments(
        payer_id=user.id,
        **payment_in.model_dump()
    )

    payment = add_payment(payment , session)

    return payment
