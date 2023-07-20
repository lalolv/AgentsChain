from fastapi import APIRouter
from models.chat import ChatItem

from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import AzureChatOpenAI


router = APIRouter(prefix="/chat")

@router.post("/send")
def send_message(item: ChatItem):
    # Azure OpenAI
    model = AzureChatOpenAI(
        temperature=0.1,
        deployment_name="gpt-35-16k",
        model_name="gpt-35-turbo-16k",
        streaming=True,
        max_tokens=1024
    )
    # model(messages=messages)
    agent_chain = initialize_agent(
        tools=[DuckDuckGoSearchRun()], llm=model,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True)

    return agent_chain.run(input=item.question)
