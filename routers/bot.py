from fastapi import APIRouter
from core.database import MongoDBClient
from bson.objectid import ObjectId


router = APIRouter(prefix="/bot")


@router.get("/list")
# 获取机器人列表
async def get_bot_list():
    # Get the database
    mgocli = MongoDBClient()
    db = mgocli.getAppChainDB()
    coll_name = db.get_collection(name='bots')
    bots_list = coll_name.find()
    bots = []
    for bot in bots_list:
        bots.append({
            'id':       str(bot['_id']),
            'name':     bot['name'],
            'desc':     bot['desc'],
            'avatar':   bot['avatar'],
            'llm':      bot['llm'],
            'tools':    bot['tools'],
        })

    return bots


@router.get("/detail/{bot_id}")
async def get_bot_detail(bot_id: str):
    # Get the database
    mgocli = MongoDBClient()
    db = mgocli.getAppChainDB()
    coll = db.get_collection(name='bots')
    info = coll.find_one({'_id': ObjectId(bot_id)})
    if info is None:
        return None

    return {
        'name':     info["name"],
        'desc':     info['desc'],
        'avatar':   info['avatar'],
        'llm':      info['llm'],
        'tools':    info['tools'],
        'prompts':  info['prompts'],
    }
