"""Tool for the DuckDuckGo search API."""

from typing import Optional

from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper


class DuckDuckGoSearchRun(BaseTool):
    """Tool that queries the DuckDuckGo search API."""

    name = "duckduckgo_search"
    description = (
        "A wrapper around DuckDuckGo Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query. "
        "Please answer in the same language as the user. "
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)
    
    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return self.api_wrapper.run(query)