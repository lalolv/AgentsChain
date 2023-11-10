from core.cache import agents
from models.agent import AgentItem


# 获取机器信息
def get_bot_info(bot_id: str) -> AgentItem:
    global agents
    return agents[bot_id]
