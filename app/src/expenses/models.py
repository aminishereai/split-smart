from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Split(str , Enum):
    disproportionate = "disproportionate"
    equal = "equal"

# Tables 
class Expenses(SQLModel , table=True):
    id : Optional[int] = Field(index=True , default= None , primary_key=True)
    user_id : int = Field(foreign_key="users.id", ondelete="CASCADE")
    group_id : int = Field(foreign_key="groups.id", ondelete="CASCADE")
    total_amt : Decimal = Field(max_digits=10 , decimal_places=2)
    split_type : Split

class ExpenseSplit(SQLModel ,table=True) :
    user_id : int = Field(foreign_key="users.id" , primary_key=True , ondelete="CASCADE")
    expense_id : int = Field(foreign_key="expenses.id" , primary_key=True, ondelete="CASCADE")
    decided_amt : Decimal = Field(max_digits=10 , decimal_places=2) 
  
# Schemas
class ExpenseIn(SQLModel):
    group_id : int 
    total_amt : Decimal = Field(max_digits=10 , decimal_places=2)
    split_type : Split

