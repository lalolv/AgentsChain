# 机器人使用的工具
# 格式：{botid: [tool1, tool2, tool3]}
# botid: 机器人id
# tool: 本服服器使用的工具
from typing import Dict
from models.agent import AgentItem


# 本地已安装的智能体
agents: Dict[str, AgentItem] = {}
