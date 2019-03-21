from pymongo.mongo_client import MongoClient
from redis import Redis

# mongodb
MDB = MongoClient(host="127.0.0.1", port=27017)["web_chat"]

# redis服务器
RDB = Redis(8)


