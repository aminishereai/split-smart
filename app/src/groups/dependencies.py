from uuid import uuid4

from fastapi import HTTPException , status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.core.database import SessionDep
from app.src.auth.models import Users
from app.src.groups.models import Groups, GroupsIn
from app.src.groups.services import add_session


def make_group(group : GroupsIn ,session : SessionDep)-> Groups:
    try:
        group_db = Groups(
            name = group.name,
            invite_code = str(uuid4())[:10]
        )
        group_db = add_session(group_db , session)
        return group_db
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{group.name} is already taken. Try another one."
        )    

def verify_group(group_id : int , invitation_code : str , session : SessionDep):
    statement = select(Groups).where((Groups.id == group_id) and (Groups.invite_code == invitation_code))
    v_group = session.exec(statement).one_or_none()
    return v_group

