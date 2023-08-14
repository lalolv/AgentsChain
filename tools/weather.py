"""
天气接口
Tool for the OpenWeatherMap API.
"""

from typing import Optional
from langchain.tools.base import BaseTool
from langchain.utilities import OpenWeatherMapAPIWrapper
from pydantic import Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


# 天气工具
class WeatherTool(BaseTool):
    """Tool that adds the capability to query the Weather API."""

    # api_wrapper
    api_wrapper: OpenWeatherMapAPIWrapper = Field(
        default_factory=OpenWeatherMapAPIWrapper
    )

    name = "weather"
    description = (
        "A wrapper around OpenWeatherMap API. "
        "Useful for fetching current weather information for a specified location. "
        "The input should be an English string representing the location (e.g. London,GB). "
        "Please answer in the same language as the user. "
    )

    def _run(
        self, location: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        # 判断 location 的数据类型是否为字符串
        if not isinstance(location, str):
            raise TypeError("location must be a string")
         
        """Use the OpenWeatherMap tool."""
        return self.api_wrapper.run(location)

    async def _arun(
        self, location: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        # 判断 location 的数据类型是否为字符串
        if not isinstance(location, str):
            raise TypeError("location must be a string")
         
        """Use the OpenWeatherMap tool."""
        return self.api_wrapper.run(location)
    