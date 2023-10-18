from fastapi import APIRouter
from core.cache import agents

router = APIRouter(prefix="/bot")


@router.get("/list")
# 获取机器人列表
async def get_bot_list():
    global agents
    # Get the database
    bots = []
    for item in agents.values():
        bots.append(item)

    return bots


@router.get("/detail/{bot_id}")
async def get_bot_detail(bot_id: str):
    global agents
    return agents[bot_id]
