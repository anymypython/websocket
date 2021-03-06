from flask import Blueprint, jsonify, request, send_file
from uuid import uuid4
from settings import AVATAR, CHATPATH, CHATIMG
from tools import Ret
from settings import MDB
import os
import time

upload = Blueprint('upload', __name__)


@upload.route("/get_chat/<filename>")
def get_chat(filename):
    audio_path = os.path.join(CHATPATH, filename)
    return send_file(audio_path)


@upload.route('/avatar', methods=["POST"])
def avatar():
    img_file = request.files.get('reco')
    img_name = f"{uuid4()}.jpg"
    img_path = os.path.join(AVATAR, img_name)
    img_file.save(img_path)
    return jsonify({'filename': img_name})


@upload.route('/chat_img/<imgname>')
def chat_img(imgname):
    img_path = os.path.join(CHATIMG, imgname)
    return send_file(img_path)


@upload.route("/up_app_record", methods=["POST"])
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
    if to_user: # 私聊
        user_list = [from_user, to_user]
    else:  # 群聊
        user_list = [from_user]
    chat_view = MDB.chat.find_one({"user_list": user_list})
    chat_info["message"] = f"{file_name}.mp3"
    print(chat_info)
    # 聊天窗口存在
    if chat_info.get("type") == "group":
        MDB.chat.update_one({"user_list": ["group"]}, {"$push": {"chat_list": chat_info}})
    if chat_view: # 好友聊天, 已经有聊天窗口
        MDB.chat.update_one({"user_list": user_list}, {"$push": {"chat_list": chat_info}})
    else:  # 第一次聊天的用户
        MDB.chat.insert_one({"user_list": user_list, "chat_list": [chat_info]})
    res["code"] = 0
    res["msg"] = "app上传录音"
    res["data"] = {"filename": f'{file_name}.mp3'}
    return jsonify(res)  # 提示音过后手动收取


@upload.route("/up_app_img", methods=["POST"])
def up_app_img():   #图片上传
    res = Ret().dict
    reco_file = request.files.get("reco")  # 录音文件
    chat_info = request.form.to_dict()  # 聊天信息
    # chat_info = {"to_user":"123123213","from_user":"123213213212", type:msg/img, msg: msg/img}
    img_file = request.files.get('reco')
    img_name = f"{uuid4()}.jpg"
    img_path = os.path.join(CHATIMG, img_name)
    img_file.save(img_path)
    from_user = chat_info.get("from_user")
    to_user = chat_info.get("to_user")
    if to_user:
        user_list = [from_user, to_user]
    else:
        user_list = [from_user]
    chat_view = MDB.chat.find_one({"user_list": user_list})
    chat_info["message"] = img_name
    print(chat_info)
    # 聊天窗口存在
    if chat_info.get("type") == "group":
        MDB.chat.update_one({"user_list": ["group"]}, {"$push": {"chat_list": chat_info}})
    if chat_view:
        MDB.chat.update_one({"user_list": user_list}, {"$push": {"chat_list": chat_info}})
    else:
        MDB.chat.insert_one({"user_list": user_list, "chat_list": [chat_info]})
    res["code"] = 0
    res["msg"] = "app上传录音"
    res["data"] = {"filename": img_name}
    return jsonify(res)  # 提示音过后手动收取
