from flask import Blueprint, jsonify, request
from tools import Ret
from settings import MDB
import os
import time
from tools import Ret
from bson import ObjectId

chat = Blueprint('chat', __name__)


@chat.route("/chat_list", methods=["POST"])
def chat_list():  # 获取聊天记录
    res = Ret().dict
    user_list = list(request.form.to_dict().values())
    print(user_list)
    friends = MDB.chat.find({"user_list": user_list}, {"_id": 0})
    # print(list(friends))
    res["data"] = list(friends)[0].get("chat_list")
    print(res)
    return jsonify(res)
