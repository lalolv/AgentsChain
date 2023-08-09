from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import system, user, chat, bot
from models.chat import cache_tools_from_db_batch
from loguru import logger

# load env
load_dotenv()

# create app
app = FastAPI()

# 允许的访问域
origins = ["*"]
# origins = ["https://appchain.ai", "https://www.appchain.ai"]

# 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# 路由设置
app.include_router(system.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(bot.router)


@app.on_event("startup")
async def startup_event():
    logger.info('startup!')
    # 缓存
    cache_tools_from_db_batch()
