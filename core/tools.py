from typing import List, Dict, Sequence
from langchain.tools.base import BaseTool
from langchain.callbacks.base import Callbacks
from tools.search import DuckDuckGoSearchRun
from tools.horoscope import HoroscopeTool
from tools.weather import WeatherTool
from tools.wikipedia import WikipediaQueryRun
from dotenv import load_dotenv


# load env
load_dotenv()

# 加载工具
def load_tools(tool_names: List[str], callbacks: Callbacks) -> Sequence[BaseTool]:
    tools = []

    for name in tool_names:
        base_tool = _EXTRA_TOOLS[name]
        base_tool.callbacks = callbacks
        tools.append(base_tool)

    return tools


# 工具列表
_EXTRA_TOOLS: Dict[str, BaseTool] = {
    "search": DuckDuckGoSearchRun(),
    "horoscope": HoroscopeTool(),
    "weather": WeatherTool(),
    "wikipedia": WikipediaQueryRun()
}
