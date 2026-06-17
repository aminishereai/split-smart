from sqlmodel import Field, SQLModel

# Tables 
class Groups(SQLModel , table=True):
    id : int = Field(primary_key = True)
    name : str = Field(index=True)
    invite_code : str

# And the schemas ....
class GroupsCreate(SQLModel):
    name : str

