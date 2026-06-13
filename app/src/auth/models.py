from pydantic import EmailStr
from sqlmodel import Field, SQLModel

# Databases
class Users(SQLModel , table=True):
    id : int = Field(primary_key=True , nullable=False)
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
