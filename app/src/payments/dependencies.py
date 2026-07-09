
from sqlmodel import Session

from app.src.payments.models import Payments


def add_payment(payments : Payments , session : Session):
    session.add(payments)
    session.commit()
    session.refresh(payments)

    return payments

