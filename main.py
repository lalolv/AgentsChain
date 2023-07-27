from dotenv import load_dotenv
from fastapi import FastAPI
from routers import system, user, chat, bot


# load env
load_dotenv()

# create app
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# 路由设置
app.include_router(system.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(bot.router)
