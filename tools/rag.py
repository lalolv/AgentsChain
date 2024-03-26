"""Tool for the RAG search Doc."""
from typing import Optional
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema.callbacks.base import BaseCallbackManager
from langchain.utils import get_from_env


class RagRun(BaseTool):
    """Tool that queries the Doc."""

    name = "rag"
    description = (
        "Respond in Chinese. "
        "Do your best to answer the questions. "
        "Feel free to use any tools available to look up. "
        "relevant information, only if necessary. "
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
                # Model name
                emb_model = get_from_env(
                    'EMBEDDINGS_MODEL', 'EMBEDDINGS_MODEL', 'BAAI/bge-m3')
                device = get_from_env('DEVICE', 'DEVICE', 'cpu')
                # Chroma
                db = Chroma(
                    collection_name=agent_id,
                    persist_directory='vecdb',
                    embedding_function=HuggingFaceEmbeddings(
                        model_name=emb_model,
                        model_kwargs={'device': device})
                )
                docs = db.similarity_search(query)
                # 返回全路径 agents/rag/docs/state_of_the_union.txt
                # 截取最后的文档名称
                if type(self.callbacks) is BaseCallbackManager:
                    self.callbacks.add_metadata(docs[0].metadata)

                return docs[0].page_content

        return ""
