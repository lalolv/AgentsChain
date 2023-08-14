from fastapi import APIRouter, WebSocket
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, AIMessage
from langchain.callbacks.base import BaseCallbackManager
from core.tools import load_tools
from core.callbacks import ChatStreamCallbackHandler
from core.cache import bot_tools

from typing import List
from models.chat import get_tools_from_db, StreamOutput
from models.bot import get_bot_info
from utils.agent import get_agent_type


router = APIRouter(prefix="/chat")


@router.websocket("/completion/{bot_id}")
async def websocket_endpoint(websocket: WebSocket, bot_id: str):
    await websocket.accept()

    # 获取机器人信息
    bot_info = get_bot_info(bot_id)

    # Azure OpenAI
    model = AzureChatOpenAI(
        temperature=bot_info.temperature,
        deployment_name="gpt-35-16k",
        model="gpt-35-turbo-16k",
        streaming=True,
        callbacks=[ChatStreamCallbackHandler(websocket=websocket)],
        max_tokens=1024,
        client=None
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    # 消息
    # model(messages=[
    #     SystemMessage(content="Please answer in the same language as the user.")
    # ])
    agent_chain = initialize_agent(
        tools=load_tools(bot_info.tools, [
                         ChatStreamCallbackHandler(websocket=websocket)]),
        llm=model,
        callback_manager=BaseCallbackManager(
            handlers=[ChatStreamCallbackHandler(websocket=websocket)]),
        agent=get_agent_type(bot_info.agent_type),
        memory=memory, verbose=True)

    data = await websocket.receive_text()
    # tips = "Please answer in the same language as the user."
    result = await agent_chain.arun(input="{0}".format(data))
    await websocket.send_json(StreamOutput(action='result', outputs=result)._asdict())


# 获取 tools 信息
def get_tools(bot_id: str) -> List[str]:
    global bot_tools
    if bot_id not in bot_tools:
        return get_tools_from_db(bot_id)

    # 通过数据库查询
    return []
