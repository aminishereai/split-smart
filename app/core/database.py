from sqlmodel import SQLModel , create_engine

from app.core.configs import settings

engine = create_engine(str(settings.database_url))

def create_tables_and_db ():

    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e :
        raise e


