from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import agent, system, user, chat
from widgets import doc, prompt
from loguru import logger
from core.load import load_agents
from core.tools import cache_tools
from core.cache import tools

# load env
load_dotenv()

# create app
app = FastAPI()

# 允许的访问域
origins = ["*"]


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
    global tools
    print(tools)
    return {"Hello": "World"}


# 路由设置
app.include_router(system.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(agent.router)

# widgets
prefix_wr = '/widget'
app.include_router(router=doc.router, prefix=prefix_wr)
app.include_router(router=prompt.router, prefix=prefix_wr)


# Startup
@app.on_event("startup")
async def startup_event():
    logger.info('startup!')
    # 缓存工具集
    cache_tools()
    # 缓存智能体
    load_agents()
