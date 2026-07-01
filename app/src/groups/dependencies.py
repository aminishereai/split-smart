from uuid import uuid4

from fastapi import HTTPException , status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.database import SessionDep
from app.src.auth.models import Users
from app.src.groups.models import Groups, GroupsIn, Roles, UserGroupJunction
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

def delete_group(group : Groups  , user : Users, session : SessionDep)-> bool:
    statement = select(UserGroupJunction).where(UserGroupJunction.user_id == user.id , UserGroupJunction.group_id == group.id)
    junc = session.exec(statement).one_or_none()
    if not junc :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group.name} with user {user.name} not found"
        )
    
    is_admin : bool = junc.role == Roles.admin

    if not is_admin :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User : {user.name} is not authorized to delete the group {group.name}."
        )
    
    session.delete(group)
    session.commit()
    return True


def list_members(group_id : int , session : Session):
    statement = select(Users).join(UserGroupJunction).where(UserGroupJunction.group_id == group_id)
    members = session.exec(statement).all()
    
    if not members:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= f"Group with id {group_id} not found or has no members."
        )
    
    return members