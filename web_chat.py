from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket  # 语法提示
import json
from settings import MDB

app = Flask(__name__)

user_socket_dict = {}


@app.route("/ws/<nick>")
def ws(nick):
    user_socket = request.environ.get("wsgi.websocket")  # type: WebSocket
    if user_socket:
        friend_json = json.dumps({"type": 'friend', 'data': list(user_socket_dict.keys())})
        print(friend_json)
        MDB.online.insert_one({"nick": nick})
        user_socket_dict[nick] = user_socket
        user_socket.send(json.dumps({"type": 'system', "count": len(user_socket_dict)}))
        user_socket.send(friend_json)

    print(user_socket_dict)
    while 1:
        try:
            msg = user_socket.receive()  # 等待接收客户端发过来的消息
            msg = json.loads(msg)  # msg>>{to_user: A, from_user: B, message: "alex"}
            print(msg)
            to_user_socket = user_socket_dict.get(msg.get("to_user"))
            msg_json = json.dumps(msg)  # 序列化消息
            to_user_socket.send(msg_json)  # 发送消息
        except KeyError:
            user_socket_dict.pop(to_user_socket)
            print(nick, '...')
            return
        except TypeError:
            print(nick)
            [i.send({"type": "leave", "friend_id": nick, "count": len(user_socket_dict)}) for i in
             user_socket_dict.values()]
            return jsonify({})


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 9998), application=app, handler_class=WebSocketHandler)
    http_server.serve_forever()
