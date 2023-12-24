from langchain.agents import AgentType
from typing import Optional
from core.cache import agents
from models.agent import AgentItem


agent_type = {
    1: AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    2: AgentType.REACT_DOCSTORE,
    3: AgentType.SELF_ASK_WITH_SEARCH,
    4: AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    5: AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    6: AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    7: AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    8: AgentType.OPENAI_FUNCTIONS,
    9: AgentType.OPENAI_MULTI_FUNCTIONS,
}

# 获取代理类型
def get_agent_type(val: Optional[int]) -> Optional[AgentType]:
    if val is None:
        return None
    
    return agent_type[val]


# 获取代理信息
def get_agent_info(bot_id: str) -> AgentItem:
    global agents
    return agents[bot_id]
