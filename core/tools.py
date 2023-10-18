from typing import List, Sequence
from langchain.tools.base import BaseTool
from langchain.callbacks.base import Callbacks
from dotenv import load_dotenv
from models.agent import ToolItem
import importlib


# load env
load_dotenv()


def load_tools(agnt_id:str, tool_names: List[ToolItem], callbacks: Callbacks) -> Sequence[BaseTool]:
    # 加载工具
    tools = []

    for item in tool_names:
        mod = importlib.import_module("agents.{0}.{1}".format(agnt_id, item.endpoint))
        if hasattr(mod, item.classname):
            ToolClass = getattr(mod, item.classname)
            base_tool = ToolClass()
            base_tool.callbacks = callbacks
            tools.append(base_tool)

    return tools
