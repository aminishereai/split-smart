from datetime import timedelta , datetime

import jwt
from passlib.context import CryptContext
from sqlmodel import select

from app.core import configs
from app.core.database import SessionDep
from app.src.auth.models import Token, Users

SECRET_KEY = configs.settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = configs.settings.access_token_expire_minutes
ALGORITHM = configs.settings.algorithm

pwd_context = CryptContext(
    ["argon2"],
    deprecated = "auto"
)

def hash_password (password : str) -> str:
    return pwd_context.hash(password)

def verify_password(hashed_pwd : str , pwd : str) -> bool:
    return pwd_context.verify(pwd , hashed_pwd)


def authenticate_user(
        username : str,
        password : str,
        session : SessionDep
) -> Users | None :
    
    statement = select(Users).where(Users.name == username)
    user = session.exec(statement).one_or_none()

    if not user :
        return None

    if not verify_password(
        user.hash_pwd,
        password
    ):
        return  None

    return user

def create_access_token(data: dict, exp: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    payload = data.copy()
    payload["exp"] = datetime.now() + exp

    token = jwt.encode(
        payload,
        SECRET_KEY,
        ALGORITHM
    )

    return Token(access_token=token , token_type="bearer")