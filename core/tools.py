from typing import List, Dict, Sequence
from langchain.tools.base import BaseTool
from langchain.tools import DuckDuckGoSearchRun
from tools.horoscope import HoroscopeTool
from tools.weather import WeatherTool
from dotenv import load_dotenv


# load env
load_dotenv()

# 加载工具
def load_tools(tool_names: List[str]) -> Sequence[BaseTool]:
    tools = []

    for name in tool_names:
        tools.append(_EXTRA_TOOLS[name])

    return tools


# 工具列表
_EXTRA_TOOLS: Dict[str, BaseTool] = {
    "search": DuckDuckGoSearchRun(),
    "horoscope": HoroscopeTool(),
    "weather": WeatherTool(),
}
