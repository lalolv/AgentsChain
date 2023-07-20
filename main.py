from dotenv import load_dotenv
from fastapi import FastAPI
from routers import user, chat


# load env
load_dotenv()

# create app
app = FastAPI()

# 路由设置
app.include_router(user.router)
app.include_router(chat.router)
