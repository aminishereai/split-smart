from typing import Any

from sqlmodel import SQLModel, Session


def add_session(entity : SQLModel , session :Session ) -> Any:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity