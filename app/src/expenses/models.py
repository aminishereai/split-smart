from decimal import Decimal
from enum import Enum
from typing import  Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class Split(str , Enum):
    disproportionate = "disproportionate"
    equal = "equal"

class SplitIn(SQLModel):
    user_id :int
    percentage : int = Field(ge=0, le=100)

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
    total_amt : Decimal = Field(max_digits=10 , decimal_places=2)
    split_type : Split
    splits : Optional[list[SplitIn]] = None


    @model_validator(mode="after")
    def validate_split(self):
        if self.split_type == Split.disproportionate :
            if not self.splits :
                raise ValueError("Splits of individual users required for disproportionate split.")
            
            total = sum(x.percentage for x in self.splits)
            if abs(total - 100) > 0.01 :
                raise ValueError("Percentage must sum to 100")
            
        if self.split_type == Split.equal :
            if self.splits :
                raise ValueError("Splits not required for equal split.")
        
        return self

