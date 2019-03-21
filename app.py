from flask import Flask
from blunp.user import user

app = Flask(__name__)
app.register_blueprint(user)
if __name__ == '__main__':
    app.run("0.0.0.0", 8888, debug=True)
