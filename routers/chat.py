import os
from fastapi import APIRouter, WebSocket
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama
from langchain.callbacks.base import BaseCallbackManager
from core.tools import load_tools
from core.callbacks import ChatStreamCallbackHandler
from utils.agent import get_agent_info
from fastapi import WebSocket, WebSocketDisconnect
from loguru import logger
from typing import List
from dotenv import load_dotenv
from models.agent import AgentItem


# load env
load_dotenv()
# router
router = APIRouter(prefix="/chat")


# Use a local model through Ollama
model_name = os.environ.get('OPENAI_MODEL_NAME')
logger.debug('Model: {0}'.format(model_name))


# callbacks: Callbacks = callback_mgr
llm = Ollama(model=model_name)

# Connection Manager
class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, ws: WebSocket, agent_info: AgentItem):
        # callbacks
        chat_callback = ChatStreamCallbackHandler(ws)
        callback_mgr = BaseCallbackManager([chat_callback])
        llm.callbacks = callback_mgr
        # bluesky4cn/react-chat
        # hwchase17/react
        # hwchase17/react-chat-json
        prompt = hub.pull("bluesky4cn/react-chat")
        # Construct the ReAct agent
        # tools = [TavilySearchResults(max_results=1)]
        tools = load_tools(agent_info.agent_id, agent_info.tools, callback_mgr)
        agent = create_react_agent(llm, tools, prompt)
        # Create an agent executor by passing in the agent and tools
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True,
            callback_manager=callback_mgr,
            handle_parsing_errors=True)
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        self.active_connections.remove(ws)

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    async def send_message(self, message: str):
        # stream output
        # "chat_history": ''
        input = {"input": message, "chat_history": ''}
        await self.agent_executor.ainvoke(input)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message)


# Manager Object
manager = ConnectionManager()

@router.websocket("/completion/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    # 获取机器人信息
    agent_info = get_agent_info(agent_id)
    logger.debug('Agent: {0}, {1}'.format(agent_id, agent_info.name))
    # Connect
    await manager.connect(websocket, agent_info)
    # Broadcast message
    await manager.broadcast(f"Welcome!")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Bye!")
