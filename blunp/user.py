import time
from flask import Blueprint, request, jsonify
from tools import Ret
from settings import MDB

user = Blueprint("user", __name__)


@user.route("/login", methods=["POST"])
def login():
    res = Ret().dict
    print(res)
    login_info = request.form.to_dict()
    login_user = MDB.user.find_one(login_info)
    print(login_user)
    res['data'] = {"_id": str(login_user.get("_id"))}
    return jsonify(res)


@user.route("/reg", methods=["POST"])
def reg():
    res = Ret().dict
    print(res)
    reg_info = request.form.to_dict()
    print(reg_info)
    user_reg = MDB.user.insert_one(reg_info)
    res['msg'] = "注册成功"
    return jsonify(res)
