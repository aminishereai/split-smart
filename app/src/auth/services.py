from passlib.context import CryptContext
from sqlmodel import select

from app.core.database import SessionDep
from app.src.auth.models import Users


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

