"""Tool for the DuckDuckGo search API."""
from duckduckgo_search import DDGS
from typing import List, Optional
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool


class DuckDuckGoSearchRun(BaseTool):
    """Tool that queries the DuckDuckGo search API."""

    name = "duckduckgo_search"
    description = (
        "A wrapper around DuckDuckGo Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query. "
        "Please answer in the same language as the user. "
    )

    region: str = "wt-wt"
    safesearch: str = "moderate"
    time: Optional[str] = "y"
    max_results: int = 5

    def get_snippets(self, query: str) -> List[str]:
        """Run query through DuckDuckGo and return concatenated results."""

        with DDGS() as ddgs:
            results = ddgs.text(
                query,
                region=self.region,
                safesearch=self.safesearch,
                timelimit=self.time,
            )
            if results is None:
                return ["No good DuckDuckGo Search Result was found"]
            snippets = []
            for i, res in enumerate(results, 1):
                if res is not None:
                    snippets.append(res["body"])
                if len(snippets) == self.max_results:
                    break
        return snippets

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return ""

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        snippets = self.get_snippets(query)
        return " ".join(snippets)
