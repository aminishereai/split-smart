from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlmodel import select

from app.core.database import SessionDep
from app.src.auth.models import Token, Users, UsersCreate
from app.src.auth.services import ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, hash_password

credentials_exception = lambda name , **kwargs :  HTTPException(
    status_code= status.HTTP_401_UNAUTHORIZED,
    detail= f"{name} is not authorized",
    **kwargs
)

oauth2_scheme = OAuth2PasswordBearer("auth/login/")

def get_current_user(token : Annotated[str , Depends(oauth2_scheme)] , session : SessionDep) -> Users:
    cred_exp = credentials_exception("User" , headers={"WWW-Authenticate": "Bearer"})
    try : 
        payload = jwt.decode(token , SECRET_KEY , [ALGORITHM])
        username = payload.get("sub")
        statement = select(Users).where(Users.name == username)
        user = session.exec(statement).one_or_none()
        # Checks for existing user
        if not user :
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail = f"Username : {username} does not Exists"
            )
        
        return user

    except Exception:
        raise cred_exp
    

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
CurrentUserDep = Annotated[Users , Depends(get_current_user) ]