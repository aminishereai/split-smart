from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.core.database import SessionDep
from app.src.auth.models import Token, Users, UsersCreate
from app.src.auth.services import authenticate_user, create_access_token

credentials_exception = lambda name :  HTTPException(
    status_code= status.HTTP_401_UNAUTHORIZED,
    detail= f"{name} is not authorized"
)




def create_user(user : UsersCreate , session : SessionDep)-> Users:
    statement = select(Users).where(Users.name == user.name)
    existing_user = session.exec(statement).one_or_none()
    # Checks for existing user
    if existing_user :
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail = f"Username : {user.name} already Exists"
        )
    # Creates new user
    user_db = Users.model_validate(user)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    #Now comes the login part

    authenticated_user = authenticate_user(
        username=user.name,
        password=user.password,
        session=session
    )
    if not authenticated_user:
        raise credentials_exception(user.name)
    
    return authenticated_user


def login_user(
        form_data : Annotated[OAuth2PasswordRequestForm , Depends()],
        session : SessionDep,
) -> Users:
    authenticated_user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        session=session
    )
    if not authenticated_user:
        raise credentials_exception(form_data.username)
    
    return authenticated_user






LoginUserDep = Annotated[Users , Depends(login_user) ]
CreateUserDep = Annotated[Users , Depends(create_user) ]