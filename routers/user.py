from fastapi import APIRouter
from models.user import UserSchemas
from core.cache import bot_tools


router = APIRouter(prefix="/user")


@router.get("/info/{username}")
def get_user(username: str):
    # user = user_services.get_user_by_username(username)
    return UserSchemas(username=username, fullname=username, password='123')


@router.post("/login")
# 用户登陆
def login():
    global bot_tools
    bot_tools['bot-1'] = ['search', 'math']
    
    return 'ok'


@router.post("/register")
# 用户注册
def register():
    global bot_tools
    return bot_tools.get('bot-1')
