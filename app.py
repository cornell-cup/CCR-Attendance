from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import sys
sys.path.insert(0, os.getcwd()+"/src")
import CCRAttendance


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/')
def index():
    print("what's going on")
    return render_template("index.html", title = "Welcome")

@socketio.on('send_message')
def handle_source(json_data):
    print(json_data)
    text = json_data['message']
    socketio.emit('echo', {'echo': 'Server Says: '+text})

if __name__ == '__main__':
    socketio.run(app)