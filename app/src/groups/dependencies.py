from uuid import uuid4

from app.core.database import SessionDep
from app.src.auth.models import Users
from app.src.groups.models import Groups, GroupsIn


def make_group(group : GroupsIn ,session : SessionDep)-> Groups:
    group_db = Groups.model_validate(group)
    group_db.invite_code = str(uuid4())[:10]
    session.add(group_db)
    session.commit()
    session.refresh(group_db)
    return group_db
