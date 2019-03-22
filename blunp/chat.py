from flask import Blueprint, jsonify, request
from tools import Ret
from settings import MDB, CHATPATH
import os
import time
from tools import Ret
from bson import ObjectId

chat = Blueprint('chat', __name__)


@chat.route("/chat_list", methods=["POST"])
def chat_list():
    res = Ret().dict
    friends = MDB.online.find({}, {"_id": 0})
    # print(list(friends))
    res["data"] = list(friends)
    return jsonify(res)


@chat.route("/up_app_record", methods=["POST"])
def up_app_record():
    res = Ret().dict
    reco_file = request.files.get("reco")  # 录音文件
    chat_info = request.form.to_dict()  # 聊天信息
    # chat_info = {"to_user":"123123213","from_user":"123213213212", type:msg/img, msg: msg/img}
    file_name = reco_file.filename
    reco_file_path = os.path.join(CHATPATH, file_name)
    reco_file.save(reco_file_path)

    # 录音格式转换 >>web页面只能播放.mp3格式的音乐文件
    os.system(f"ffmpeg -y -i {reco_file_path} {reco_file_path}.mp3")
    os.remove(reco_file_path)  # 清除原录音文件, 省空间
    # 存储聊天记录在DB
    from_user = chat_info.get("from_user")
    to_user = chat_info.get("to_user")
    chat = {
        "from_user": chat_info.get("from_user"),
        "message": f"{file_name}.mp3",  # 聊天信息(文件名)
        "create_time": time.time()
    }
    print(chat)
    user_list = []
    print(user_list)
    chat_view = MDB.chat.find_one({"user_list": user_list})
    if chat_view:
        if chat_info.get("type") == "group":
            MDB.chat.update_one({"user_list": ["group"]}, {"$push": {"chat_list": chat}})
        else:
            MDB.chat.update_one({"user_list": user_list}, {"$push": {"chat_list": chat}})

    else:
        MDB.chat.insert_one({"user_list": user_list, "chat_lsit": [chat]})
    res["code"] = 0
    res["msg"] = "app上传录音"
    res["data"] = {"filename": chat.get('message')}
    return jsonify(res)  # 提示音过后手动收取
