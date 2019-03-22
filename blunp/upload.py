from flask import Blueprint, jsonify, request
from uuid import uuid4
from settings import AVATAR
from tools import Ret
from settings import MDB
import os

upload = Blueprint('upload', __name__)


@upload.route('/avatar', methods=["POST"])
def avatar():
    img_file = request.files.get('reco')
    img_name = f"{uuid4()}.jpg"
    img_path = os.path.join(AVATAR, img_name)
    img_file.save(img_path)
    return jsonify({'filename': img_name})
