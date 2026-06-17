from fastapi import APIRouter, HTTPException, Request , status
from psycopg2 import IntegrityError
from sqlmodel import select

from app.core.database import SessionDep
from app.src.auth.dependencies import CurrentUserDep
from app.src.groups.dependencies import make_group, verify_group
from app.src.groups.models import Groups, GroupsIn, GroupsOut, UserGroupJunction, Roles
from app.src.groups.services import add_session


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)

#creating group
@router.post("/",response_model=GroupsOut , status_code=status.HTTP_201_CREATED )
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


@router.get("/{group_id}/invite/{invitation_code}")
def get_invited(group_id : int , invitation_code : str , user : CurrentUserDep , session : SessionDep):
    valid_group = verify_group(group_id , invitation_code , session)
    if not valid_group :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The group you're looking for was not found"
        )
    assert user.id and valid_group.id is not None
    try :
        junction = UserGroupJunction(
        user_id=user.id,
        group_id=valid_group.id,
        role=Roles.member
    )
        junction : UserGroupJunction = add_session(junction , session)
        return junction
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You are already the member of group : {valid_group.name}"
        )        
    
    

@router.get("/{group_id}/invite")
def invite(group_id : int , session : SessionDep , request : Request):
    statement = select(Groups.invite_code).where(Groups.id == group_id)
    code = session.exec(statement).one_or_none()
    return {
        "invitation_link" : request.url_for("get_invited" , group_id=group_id , invitation_code= code)
    }