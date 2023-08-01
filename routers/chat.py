from fastapi import APIRouter, WebSocket
from core.callbacks import ChatStreamCallbackHandler
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.base import BaseCallbackManager
from core.tools import load_tools
from core.cache import bot_tools
from typing import List
from models.chat import get_tools_from_db
from models.chat import StreamOutput


router = APIRouter(prefix="/chat")


@router.websocket("/completion/{bot_id}")
async def websocket_endpoint(websocket: WebSocket, bot_id: str):
    await websocket.accept()

    # 获取工具列表
    tools = get_tools(bot_id)
    if len(tools) <= 0:
        return await websocket.send_text("No tool")

    # Azure OpenAI
    model = AzureChatOpenAI(
        temperature=0.1,
        deployment_name="gpt-35-16k",
        model="gpt-35-turbo-16k",
        streaming=True,
        callbacks=[ChatStreamCallbackHandler(websocket=websocket)],
        max_tokens=1024,
        client=None
    )
    # model(messages=messages)
    agent_chain = initialize_agent(
        tools=load_tools(tools, [ChatStreamCallbackHandler(websocket=websocket)]), llm=model,
        callback_manager=BaseCallbackManager(
            handlers=[ChatStreamCallbackHandler(websocket=websocket)]),
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True)

    data = await websocket.receive_text()
    result = await agent_chain.arun(input=data)
    await websocket.send_json(StreamOutput(action='result', outputs=result)._asdict())


# 获取 tools 信息
def get_tools(bot_id: str) -> List[str]:
    global bot_tools
    if bot_id not in bot_tools:
        return get_tools_from_db(bot_id)

    # 通过数据库查询
    return []
