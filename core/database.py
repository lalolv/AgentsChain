from pymongo import MongoClient
from pymongo.database import Database


class MongoDBClient(object):
    # 饿汉式 单例模式
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(MongoDBClient, cls).__new__(cls)
    #     return cls.instance

    # 代理ip Redis 连接池
    def __init__(self):
        CONNECTION_STRING = "mongodb://lalo:1128@106.55.188.190:27017/?authSource=admin"
        self.mgdb = MongoClient(
            CONNECTION_STRING, connect=False, maxPoolSize=2000)

    # 获取 MongoDB 客户端
    def getMongoClient(self) -> MongoClient:
        return self.mgdb
    
    # 获取 appchain 数据库对象
    def getAppChainDB(self) -> Database:
        return self.mgdb.get_database("appchain")
