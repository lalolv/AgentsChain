from fastapi import APIRouter
from models.user import UserSchemas


router = APIRouter(prefix="/user")


@router.get("/info/{username}")
def get_user(username: str):
    # user = user_services.get_user_by_username(username)
    return UserSchemas(username=username, fullname=username, password='123')


@router.post("/login")
# 用户登陆
def login():
    return 'ok'
