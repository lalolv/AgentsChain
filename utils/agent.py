from core.cache import agents
from models.agent import AgentItem


# 获取代理信息
def get_agent_info(bot_id: str) -> AgentItem:
    global agents
    return agents[bot_id]
