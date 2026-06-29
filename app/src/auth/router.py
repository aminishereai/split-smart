from fastapi import APIRouter , status


from app.src.auth import models
from app.src.auth.dependencies import CreateUserDep, CurrentUserDep, LoginUserDep
from app.src.auth.services import create_access_token


router = APIRouter(
    prefix = "/auth",
    tags=["Authentication" , "User"]
)

# For Creating user
@router.post("/create" ,  response_model=models.Token , status_code=status.HTTP_201_CREATED)
def create_user(user : CreateUserDep):
    data = {"sub" : user.name}

    return create_access_token(data)

@router.post("/login" , response_model=models.Token)
def login(user : LoginUserDep):
    data = {"sub" : user.name}

    return create_access_token(data)


@router.get("/me" , response_model=models.UsersOut)
def get_me(me : CurrentUserDep):
    return me



