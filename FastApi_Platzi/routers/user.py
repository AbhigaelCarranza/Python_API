from fastapi import APIRouter,status
from pydantic import BaseModel
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse

user_router = APIRouter()

##User login
class User(BaseModel):
    email:str
    password:str

##Login
@user_router.post(
    path='/login', 
    tags=['auth'],
    status_code=status.HTTP_200_OK
    )
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)
