from fastapi import APIRouter , status

from app.core.database import SessionDep
from app.src.auth.dependencies import CurrentUserDep
from app.src.groups.dependencies import make_group
from app.src.groups.models import GroupsIn, GroupsOut, UserGroupJunction, Roles


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
    session.add(junction)
    session.commit()
    session.refresh(junction)


    return junction

