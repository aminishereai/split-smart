from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel

# Tables
class Payments(SQLModel , table=True):
    id : Optional[int] = Field(default=None ,primary_key=True)
    payer_id : int = Field(foreign_key="users.id")
    lender_id : int = Field(foreign_key="users.id")
    payed_amt : Decimal = Field(max_digits=10 , decimal_places=2)


# Schemas
class PaymentsCreate(SQLModel):
    lender_id : int
    payed_amt : Decimal = Field(max_digits=10 , decimal_places=2)
    

class PaymentsOut(SQLModel):
    id : int
    payer_id : int
    lender_id : int
    payed_amt : Decimal

class Balance(SQLModel):
    balance : Decimal | int