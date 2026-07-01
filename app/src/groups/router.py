from typing import List

from fastapi import APIRouter, HTTPException, Request , status
from sqlmodel import select

from app.core.database import SessionDep
from app.src.auth.dependencies import CurrentUserDep
from app.src.auth.models import UsersOut
from app.src.groups.dependencies import delete_group, list_groups, list_members, make_group, verify_group
from app.src.groups.models import Groups, GroupsIn, GroupsOut, UserGroupJunction, Roles
from app.src.groups.services import add_session


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)

#creating group
@router.post("/",response_model=UserGroupJunction , status_code=status.HTTP_201_CREATED )
def create_group(group : GroupsIn, session: SessionDep, user : CurrentUserDep):
    group_db = make_group(group , session)

    assert user.id and group_db.id is not None

    junction = UserGroupJunction(
        user_id=user.id,
        group_id=group_db.id,
        role=Roles.admin
    )
    junction : UserGroupJunction = add_session(junction , session)


    return junction


@router.get("/" , response_model=List[GroupsOut])
def get_groups(session : SessionDep , user : CurrentUserDep):
    groups = list_groups(session , user)
    return groups


@router.get("/{group_id}/invite/{invitation_code}")
def get_invited(group_id : int , invitation_code : str , user : CurrentUserDep , session : SessionDep):
    valid_group = verify_group(group_id , invitation_code , session)
    if not valid_group :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The group you're looking for was not found"
        )
    assert user.id and valid_group.id is not None
    
    # Check if user is already a member
    existing = select(UserGroupJunction).where(
        UserGroupJunction.user_id == user.id,
        UserGroupJunction.group_id == group_id
    )
    if session.exec(existing).one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You are already a member of group : {valid_group.name}"
        )
    
    junction = UserGroupJunction(
        user_id=user.id,
        group_id=valid_group.id,
        role=Roles.member
    )
    junction = add_session(junction , session)
    return junction        
    
    

@router.get("/{group_id}/invite")
def invite(group_id : int , session : SessionDep , request : Request , user : CurrentUserDep):
    # Check if user is in the group
    assert user.id is not None
    statement = select(UserGroupJunction).where(
        UserGroupJunction.user_id == user.id,
        UserGroupJunction.group_id == group_id
    )
    membership = session.exec(statement).one_or_none()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not a member of this group"
        )
    
    # Get the invitation code
    statement = select(Groups.invite_code).where(Groups.id == group_id)
    code = session.exec(statement).one_or_none()
    
    return {
        "invitation_link" : request.url_for("get_invited" , group_id=group_id , invitation_code= code)
    }


@router.get("/{group_id}/members" , response_model=List[UsersOut])
def list_users(group_id : int ,user : CurrentUserDep, session : SessionDep):
    members = list_members(group_id , session)
    if not user in members :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User : {user.name} is not in the group with id : {group_id}."
        )
    return members


@router.delete("/{group_id}")
def del_group(group_id : int , session : SessionDep , user : CurrentUserDep ):
    statement = select(Groups).where(Groups.id == group_id)
    group = session.exec(statement).one_or_none()

    if not group :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )

    deleted = delete_group(group , user , session)
    return {"deleted" : deleted }
