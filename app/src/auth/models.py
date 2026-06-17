from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

# Databases
class Users(SQLModel , table=True):
    id : Optional[int] = Field(default= None ,primary_key=True)
    name : str
    email : EmailStr
    hash_pwd : str



# Schemas
class UsersCreate(SQLModel):
    name : str
    email : EmailStr
    password : str

class UsersOut(SQLModel):
    id : int
    name : str
    email : EmailStr

class Token(SQLModel):
    access_token : str
    token_type : str

class TokenData(SQLModel):
    id : int | None = None
    username : str | None = None
