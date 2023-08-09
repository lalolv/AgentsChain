from pydantic import BaseModel
from typing import Union, NamedTuple
from core.database import MongoDBClient
from core.cache import bot_tools
from bson.objectid import ObjectId
from typing import List
from loguru import logger


class ChatItem(BaseModel):
    question: str

# stream 输出


class StreamOutput(NamedTuple):
    action: str
    outputs: Union[str, None] = ''


# 获取单个机器人的工具列表
def get_tools_from_db(bot_id: str) -> List[str]:
    mgocli = MongoDBClient()
    db = mgocli.getAppChainDB()
    coll = db.get_collection(name='bots')
    info = coll.find_one({'_id': ObjectId(bot_id)})
    if info is None:
        return []

    return info['tools']

# 批量缓存机器人的工具列表
def cache_tools_from_db_batch():
    mgocli = MongoDBClient()
    db = mgocli.getAppChainDB()
    coll = db.get_collection(name='bots')
    infos = coll.find()
    global bot_tools
    for info in infos:
        bot_tools[info['_id']] = info['tools']
    logger.info("Cached {} bots".format(len(bot_tools)))
    