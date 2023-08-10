from langchain.agents import AgentType


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
def get_agent_type(val: int) -> AgentType:
    return agent_type[val]
