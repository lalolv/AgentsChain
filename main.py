from core.database import MongoDBClient
from dotenv import load_dotenv
from fastapi import FastAPI
from routers import system, user, chat


# load env
load_dotenv()

# create app
app = FastAPI()

# 默认路径


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/mgo")
async def read_mgo():
    # Get the database
    mgocli = MongoDBClient()
    mgoclient = mgocli.getMongoClient()
    db = mgoclient.get_database(name='appchain')
    coll_name = db.get_collection(name='bots')
    bots_list = coll_name.find()
    bots = []
    for bot in bots_list:
        bots.append({
            'name': bot['name'],
            'desc': bot['desc'],
        })

    return bots


# 路由设置
app.include_router(system.router)
app.include_router(user.router)
app.include_router(chat.router)
