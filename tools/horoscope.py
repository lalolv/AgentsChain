"""
星座运势接口
"""

import requests
from typing import Optional, Type
from langchain.tools.base import BaseTool
from pydantic import BaseModel, Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class HoroscopeSchema(BaseModel):
    name: str = Field(description="should be the English name of the constellation, such as aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces.")
    time: str = Field(description="Should be the English name of a time, such as today, nextday, week, month, year, etc.")


# 星座工具
class HoroscopeTool(BaseTool):
    """Tool that adds the capability to query the horoscope API."""


    name = "horoscope"
    description = (
        "useful for when you need to answer questions about horoscope. "
        "Please answer in the same language as the user. "
    )
    args_schema: Type[HoroscopeSchema] = HoroscopeSchema

    # 请求接口查询
    # https://api.vvhan.com/api/horoscope
    def _req_api(self, name: str, time: str = 'today') -> str:
        if name == '':
            return "error"
            
        # 访问接口
        resp = requests.get(
            url="https://api.vvhan.com/api/horoscope", 
            params={"type":name.lower(), "time":time.lower()})
        # 请求错误
        if resp.status_code != 200:
            return "error"
        # 解析json
        result = resp.json()
        success = result["success"]
        if not success:
            return "failed"
        # 返回结果
        data = result["data"]
        fortunetext = data["fortunetext"]
        fortune_all = fortunetext["all"]
        fortune_love = fortunetext["love"]
        fortune_work = fortunetext["work"]
        fortune_money = fortunetext["money"]
        fortune_health = fortunetext["health"]
        return (
            f"综合运势: {fortune_all}"
            f"爱情运势: {fortune_love}"
            f"学业工作: {fortune_work}"
            f"财富运势: {fortune_money}"
            f"健康运势: {fortune_health}"
        )

    def _run(
        self, name: str, time: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self._req_api(name=name, time=time)

    async def _arun(
        self, name: str, time: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return self._req_api(name=name, time=time)
    