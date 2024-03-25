"""
天气接口
Tool for the OpenWeatherMap API.
"""

from typing import Any, Optional
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun
)
from langchain.utils import get_from_env
from pyowm import OWM
from loguru import logger


# 天气工具
class WeatherTool(BaseTool):
    """Tool that adds the capability to query the Weather API."""

    name = "weather"
    description = (
        "A wrapper around OpenWeatherMap API. "
        "Useful for fetching current weather information for a specified location. "
        "Input should be a English location string (e.g. London,GB). "
    )

    def _format_weather_info(self, location: str, w: Any) -> str:
        detailed_status = w.detailed_status
        wind = w.wind()
        humidity = w.humidity
        temperature = w.temperature("celsius")
        rain = w.rain
        heat_index = w.heat_index
        clouds = w.clouds

        return (
            f"In {location}, the current weather is as follows:\n"
            f"Detailed status: {detailed_status}\n"
            f"Wind speed: {wind['speed']} m/s, direction: {wind['deg']}°\n"
            f"Humidity: {humidity}%\n"
            f"Temperature: \n"
            f"  - Current: {temperature['temp']}°C\n"
            f"  - High: {temperature['temp_max']}°C\n"
            f"  - Low: {temperature['temp_min']}°C\n"
            f"  - Feels like: {temperature['feels_like']}°C\n"
            f"Rain: {rain}\n"
            f"Heat index: {heat_index}\n"
            f"Cloud cover: {clouds}%"
        )
    
    def _run(
        self, location: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        return ""

    async def _arun(
        self, location: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        logger.debug('Loc: {0}'.format(location))
        # 判断 location 的数据类型是否为字符串
        if not isinstance(location, str):
            raise TypeError("location must be a string")
        
        # 获取环境变量中的 api key
        openweathermap_api_key = get_from_env(
            "openweathermap_api_key", "OPENWEATHERMAP_API_KEY"
        )
        
        owm = OWM(openweathermap_api_key)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        if observation == None:
            return ""
        
        return self._format_weather_info(location, observation.weather)
    