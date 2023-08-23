from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import mii, system, user, chat, bot
from loguru import logger

# load env
load_dotenv()

# create app
app = FastAPI()

# 允许的访问域
# origins = ["*"]
origins = [
    "http://192.168.3.15:5173", 
    "http://127.0.0.1:5173", 
    "https://appchain.ai", 
    "https://www.appchain.ai",
    "https://mii.appchain.ai"
]


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
app.include_router(mii.router)


@app.on_event("startup")
async def startup_event():
    logger.info('startup!')
