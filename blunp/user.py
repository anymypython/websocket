import time

from flask import Blueprint, request, jsonify
from tools import Ret
from settings import MDB
from bson import ObjectId
import os
user = Blueprint("user", __name__)


@user.route("/login", methods=["POST"])
def login():
    res = Ret().res
    print(res)
    login_info = request.form.to_dict()
    login_user = MDB.user.find_one(login_info)
    print(login_user)
    res['data'] = {"_id": str(login_user.get("_id"))}
    return jsonify(res)


@user.route("/reg", methods=["POST"])
def reg():
    res = Ret().res
    print(res)
    reg_info = request.form.to_dict()
    user_reg = MDB.user.insert_one(reg_info)
    res['msg'] = "注册成功"
    return jsonify(res)


@user.route("/chat_list", methods=["POST"])
def chat_list():
    res = Ret().res
    friends = MDB.online.find({}, {"_id": 0})
    # print(list(friends))
    res["data"] = list(friends)
    return jsonify(res)


@user.route("/up_app_record", methods=["POST"])
def up_app_record():
    reco_file = request.files.get("reco")  # 录音文件
    chat_info = request.form.to_dict()  # 聊天信息
    # chat_info = {"chat_id":"123213213","to_user":"123123213","from_user":"123213213212"}
    file_name = reco_file.filename
    reco_file_path = os.path.join('chat', file_name)
    reco_file.save(reco_file_path)

    # 录音格式转换 >>web页面只能播放.mp3格式的音乐文件
    os.system(f"ffmpeg -y -i {reco_file_path} {reco_file_path}.mp3")
    os.remove(reco_file_path)  # 清除原录音文件, 省空间
    # 存储聊天记录在DB
    chat = {
        "from_user": chat_info.get("from_user"),
        "message": f"{file_name}.mp3",  # 聊天信息(文件名)
        "create_time": time.time()
    }

    MDB.chats.update_one({"_id": ObjectId(chat_info.get("chat_id"))}, {"$push": {"chat_list": chat}})
    # 之间存储消息, 不做查询和修改

    # 解决消息来源问题
    # from_user app
    # to_user toy
    toy_info = MDB.toys.find_one({"_id": ObjectId(chat_info.get("to_user"))})  # 查询玩具消息
    friend_list = toy_info.get("friend_list")  # 获取玩具好友列表
    pre_tip = "No_friend.mp3"  # 好友不存在, 对方非好友
    for friend in friend_list:
        if friend.get("friend_id") == chat_info.get("from_user"):
            remark = friend.get("friend_remark")  # 获取昵称
            pre_tip = text2audio(f"你有来自{remark}的消息")  # 给好友发送消息的提示语
    set_chat(chat_info.get("to_user"), chat_info.get("from_user"))
    RET["code"] = 0
    RET["msg"] = "app上传录音"
    RET["data"] = {"filename": pre_tip}
    return jsonify(RET)  # 提示音过后手动收取
