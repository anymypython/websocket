from flask import Flask
from blunp.user import user
from blunp.chat import chat
from blunp.upload import upload

app = Flask(__name__)
app.register_blueprint(user)  # 用户登陆注册
app.register_blueprint(chat)  # 聊天记录
app.register_blueprint(upload)  # 文件上传, 响应

if __name__ == '__main__':
    app.run("0.0.0.0", 8888, debug=True)
