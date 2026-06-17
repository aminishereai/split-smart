from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.src.auth import models
from app.src.auth.dependencies import CreateUserDep


router = APIRouter(
    prefix = "auth/",
    tags=["Authentication" , "User"]
)

# For Creating user
@router.post("/create" ,  response_model=models.Token)
def create_user(token : CreateUserDep):
    return token



