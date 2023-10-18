from typing import List, Optional, Union
from pydantic import BaseModel

# 工具
class ToolItem(BaseModel):
    name: str
    endpoint: str
    classname: str

# 智能体结构
class AgentItem(BaseModel):
    agent_id: Optional[str]
    ver: Union[str, float, int] = ''
    name: Optional[str] = ''
    author: Optional[str] = ''
    desc: Optional[str] = ''
    tools: List[ToolItem] = []
    avatar: Optional[str] = ''
    temperature: Union[float, int] = 0.1
