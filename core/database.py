from pymongo import MongoClient
from pymongo.database import Database
import os


class MongoDBClient(object):
    # 单例模式
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MongoDBClient, cls).__new__(cls)
        return cls.instance

    # 代理ip Redis 连接池
    def __init__(self):
        self.mgdb = MongoClient(
            os.environ.get("MONGODB_URL"), connect=False, maxPoolSize=2000)

    # 获取 MongoDB 客户端
    def getMongoClient(self) -> MongoClient:
        return self.mgdb

    # 获取 appchain 数据库对象
    def getAppChainDB(self) -> Database:
        return self.mgdb.get_database("appchain")

    # 获取 appchain 数据库对象
    def getMiiDB(self) -> Database:
        return self.mgdb.get_database("mii")
