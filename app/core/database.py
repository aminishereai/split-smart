from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel , create_engine , Session

from app.core.configs import settings

engine = create_engine(str(settings.database_url))

def create_tables_and_db ():

    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e :
        raise e

def get_session():
    with Session(engine) as session :
        yield session

SessionDep = Annotated[Session , Depends(get_session)]
