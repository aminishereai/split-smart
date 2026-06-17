from enum import Enum
from typing import Literal, Optional

from sqlmodel import Field, SQLModel

#Seperate Enum for the roles type
class Roles(str , Enum):
    admin = "admin"
    member = "member"

# Tables 
class Groups(SQLModel , table=True):
    id : Optional[int] = Field(default = None ,primary_key = True)
    name : str = Field(index=True, unique=True)
    invite_code : Optional[str] = None

class UserGroupJunction(SQLModel , table= True):
    user_id : int = Field(foreign_key="users.id", primary_key=True, ondelete="CASCADE")
    group_id : int = Field(foreign_key="groups.id", primary_key=True, ondelete="CASCADE")
    role : Roles = Field(index=True)




# And the schemas ....
class GroupsIn(SQLModel):
    name : str

class GroupsOut(SQLModel):
    id : int
    name : str



