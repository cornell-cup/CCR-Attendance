from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import os
import sys
sys.path.insert(0, os.getcwd()+"/src")
import CCRAttendance


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html", title = "Welcome")

@socketio.on('json')
def handle_json(json):
    send(json, json = True)


if __name__ == '__main__':
    socketio.run(app)