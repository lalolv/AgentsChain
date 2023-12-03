from models.chat import StreamOutput
from langchain.callbacks.base import AsyncCallbackHandler
from typing import Dict, Any, List, Optional
from langchain.schema import AgentAction
from fastapi import WebSocket
from langchain.schema.agent import AgentFinish
from langchain.schema.output import LLMResult
from loguru import logger
from langchain.schema.messages import BaseMessage
from uuid import UUID


class ChatStreamCallbackHandler(AsyncCallbackHandler):
    # websocket
    ws: WebSocket

    # 构造函数
    def __init__(self, websocket: WebSocket) -> None:
        self.ws = websocket

    # 错误处理
    async def on_error(self, error, **_):
        print(f"on_error: {error}")
        await self.ws.send_json(StreamOutput(action='error', outputs=error))
        await self.ws.close(1001, error)

    on_tool_error = on_error
    on_llm_error = on_error
    on_chain_error = on_error

    # LLM start
    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], metadata: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Any:
        logger.info(f"[llm_start]")
        await self.ws.send_json(StreamOutput(action='llm_start')._asdict())

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        logger.info(f"[llm_end]")
        await self.ws.send_json(StreamOutput(action='llm_end')._asdict())

    async def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.info(f"[on_chat_model_start]")
        
    # LLM token
    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        await self.ws.send_json(StreamOutput(action='token', outputs=token)._asdict())

    # chain start
    async def on_chain_start(
        self, serialized: Dict[str, Any], 
        inputs: Dict[str, Any], 
        metadata: Optional[Dict[str, Any]] = None, 
        **kwargs: Any
    ) -> Any:
        logger.info(f"[chain_start]")
        await self.ws.send_json(StreamOutput(action='chain_start')._asdict())

    # chain end
    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        logger.info(f"[chain_end]")
        await self.ws.send_json(StreamOutput(action='chain_end')._asdict())

    #  Tool start
    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, metadata: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Any:
        logger.info(f"[tool_start]:{serialized['name']}")
        await self.ws.send_json(StreamOutput(action='tool_start', outputs=serialized['name'])._asdict())

    async def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        logger.info(f"[tool_end]: {tags}, {run_id}, {parent_run_id}, {kwargs}")
        await self.ws.send_json(StreamOutput(action='tool_end')._asdict())

    # agent
    async def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        logger.info(f"[agent_action]: {action.tool}")
        await self.ws.send_json(StreamOutput(action='agent_action', outputs=action.tool)._asdict())

    # agent finish
    async def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        ret = finish.return_values
        logger.info(f"on_agent_finish")
        await self.ws.send_json(StreamOutput(action='on_agent_finish', outputs=ret['output'])._asdict())

    async def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on retriever start."""
        logger.info(f"on_retriever_start")
