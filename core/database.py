from pymongo import MongoClient


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

    # 获取MongoDB这一套API
    def getMongoClient(self) -> MongoClient:
        return self.mgdb
