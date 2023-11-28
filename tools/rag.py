"""Tool for the RAG search Doc."""
from typing import Optional
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


class RagRun(BaseTool):
    """Tool that queries the Doc."""

    name = "rag"
    description = (
        "Do your best to answer the questions. "
        "Feel free to use any tools available to look up "
        "relevant information, only if necessary"
    )

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
        if self.metadata is not None:
            agent_id = str(self.metadata['agent_id'])
            if agent_id != "":
                db = Chroma(
                    collection_name=agent_id,
                    persist_directory='vecdb',
                    embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                )
                docs = db.similarity_search(query)
                # 返回全路径 agents/rag/docs/state_of_the_union.txt
                # 截取最后的文档名称
                print('Set source....')
                if run_manager is not None:
                    run_manager.metadata = {'source': 'state_of_the_union.txt'}
                self.metadata = {'source': 'state_of_the_union.txt'}
                return docs[0].page_content

        return ""
