from fastapi import APIRouter, WebSocket
# from asyncio.queues import Queue
from models.chat import ChatItem
from core.callbacks import ChatStreamCallbackHandler
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.base import BaseCallbackManager


router = APIRouter(prefix="/chat")

@router.post("/send")
def send_message(item: ChatItem):
    # Azure OpenAI
    model = AzureChatOpenAI(
        temperature=0.1,
        deployment_name="gpt-35-16k",
        model_name="gpt-35-turbo-16k",
        streaming=False,
        max_tokens=1024
    )
    # model(messages=messages)
    agent_chain = initialize_agent(
        tools=[DuckDuckGoSearchRun()], llm=model,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True)

    return agent_chain.run(input=item.question)


@router.websocket("/completion")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 声明一个队列
    # q_stream = Queue()
    # Azure OpenAI
    model = AzureChatOpenAI(
        temperature=0.1,
        deployment_name="gpt-35-16k",
        model_name="gpt-35-turbo-16k",
        streaming=True,
        callbacks=[ChatStreamCallbackHandler(websocket=websocket)],
        max_tokens=1024
    )
    # model(messages=messages)
    agent_chain = initialize_agent(
        tools=[DuckDuckGoSearchRun()], llm=model,
        callback_manager=BaseCallbackManager(
            handlers=[ChatStreamCallbackHandler(websocket=websocket)]),
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True)

    data = await websocket.receive_text()
    response = await agent_chain.arun(input=data)

    await websocket.send_text(response)
