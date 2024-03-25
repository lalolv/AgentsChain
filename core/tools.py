from typing import List, Sequence
from langchain.tools.base import BaseTool
from langchain.callbacks.base import Callbacks
from dotenv import load_dotenv
from models.agent import ToolItem
from core.cache import tools
import importlib
import yaml


# load env
load_dotenv()


def load_tools(agent_id: str, tool_names: List[str], callbacks: Callbacks) -> Sequence[BaseTool]:
    global tools
    # 加载工具
    use_tools = []

    for tool_name in tool_names:
        tool_item = tools[tool_name]
        mod = importlib.import_module("{0}".format(tool_item.endpoint))
        if hasattr(mod, tool_item.classname):
            ToolClass = getattr(mod, tool_item.classname)
            base_tool = ToolClass()
            base_tool.callbacks = callbacks
            base_tool.metadata = {"agent_id": agent_id}
            use_tools.append(base_tool)

    return use_tools


def cache_tools():
    global tools
    # 读取 yaml 配置文件信息
    with open("./tools/tools.yaml", "r") as stream:
        tools_info = yaml.full_load(stream)
        for key, val in dict(tools_info).items():
            tools[key] = ToolItem(
                name=key,
                endpoint=val['endpoint'],
                classname=val['classname']
            )
