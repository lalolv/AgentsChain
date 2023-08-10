from bson.objectid import ObjectId
from core.database import MongoDBClient
from typing import List, Union
from pydantic import BaseModel


# 机器人结构
class BotItem(BaseModel):
    id: str
    name: str = ''
    desc: str = ''
    tools: List[str] = []
    avatar: str = ''
    llm: str = ''
    agent_type: int = 1
    temperature: float = 0.1


# 获取机器信息
def get_bot_info(bot_id: str) -> BotItem:
    # Get the database
    mgocli = MongoDBClient()
    db = mgocli.getAppChainDB()
    coll = db.get_collection(name='bots')

    info = coll.find_one({'_id': ObjectId(bot_id)})
    if info is None:
        return BotItem(id=bot_id)

    return BotItem(
        id=bot_id,
        name=info['name'],
        desc=info['desc'],
        tools=info['tools'],
        avatar=info['avatar'],
        llm=info['llm'],
        agent_type=info['agent_type'],
        temperature=info['temperature'],
    )
