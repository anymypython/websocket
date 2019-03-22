from flask import Blueprint, jsonify, request
from tools import Ret
from settings import MDB
import os
import time
from tools import Ret
from bson import ObjectId

chat = Blueprint('chat', __name__)


@chat.route("/chat_list", methods=["POST"])
def chat_list():
    res = Ret().dict
    user_list = request.form.to_dict()
    print(user_list)
    friends = MDB.online.find(user_list, {"_id": 0})
    # print(list(friends))
    res["data"] = list(friends)
    print(res)
    return jsonify(res)
