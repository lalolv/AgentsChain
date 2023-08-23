from fastapi import APIRouter
from core.database import MongoDBClient


router = APIRouter(prefix="/mii")


@router.get("/avatars")
# 获取机器人列表
async def get_avatar_list(skip: int = 0, limit: int = 20):
    # Get the database
    mgocli = MongoDBClient()
    db = mgocli.getMiiDB()
    coll_name = db.get_collection(name='avatar')
    avatar_list = coll_name.find().skip(skip).limit(limit)
    avatars = []
    for item in avatar_list:
        avatars.append({
            'id': str(item['_id']),
            'key': item['key'],
            'tags': item['tags'],
            'create': item['create'],
        })
    return avatars
