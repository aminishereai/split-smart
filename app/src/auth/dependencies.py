from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlmodel import select

from app.core.database import SessionDep
from app.src.auth.exceptions import UserAlreadyExists, UserNotAuthorized, UserNotFound
from app.src.auth.models import Token, Users, UsersCreate
from app.src.auth.services import ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, hash_password
from app.utils.exceptions.base import APIException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"User is not authorized",
    headers={"WWW-Authenticate": "Bearer"}
)

oauth2_scheme = OAuth2PasswordBearer("auth/login/")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> Users:
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        username = payload.get("sub")
        statement = select(Users).where(Users.name == username)
        user = session.exec(statement).one_or_none()
        # Checks for existing user
        if not user:
            raise UserNotFound(username=username)

        return user

    except Exception as exc:
        if isinstance(exc, APIException):
            raise
        raise credentials_exception
    

def create_user(user : UsersCreate , session : SessionDep)-> Users:
    statement = select(Users).where(Users.name == user.name)
    existing_user = session.exec(statement).one_or_none()
    # Checks for existing user
    if existing_user :
        raise UserAlreadyExists(username=user.name)
    # Creates new user
    user_db = Users(
        name=user.name,
        email=user.email,
        hash_pwd=hash_password(user.password)
    )
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
        raise UserNotAuthorized(username=user.name , feature="login" )
    
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
        raise UserNotAuthorized(username=form_data.username , feature="login")
    
    return authenticated_user






LoginUserDep = Annotated[Users , Depends(login_user) ]
CreateUserDep = Annotated[Users , Depends(create_user) ]
CurrentUserDep = Annotated[Users , Depends(get_current_user) ]