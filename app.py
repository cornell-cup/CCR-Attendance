
import os
import sys
sys.path.insert(0, os.getcwd()+"/src")
import flask
from flask import Flask, render_template
import CCRAttendance
import CCRResources
from CCRResources import res

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
CCRResources.populate("res")

db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("config.json"))

def validate_key(key):
    return False #TODO: Change this to actually validate a key

@app.route('/')
def index():
    print("what's going on")
    return render_template("index.html", title = "Welcome")

@app.route("/scanners/<string:api_key>/<string:swipe_id>")
def logSwipe(api_key,swipe_id):
    if validate_key (api_key):
        db.log_swipe(swipe_id)
        data = {"key" : api_key, "ID":swipe_id, "success":True}
    else:
        data = {"key" : api_key, "ID":swipe_id, "success":False}
        return flask.jsonify(**data)
        
if __name__ == '__main__':
    socketio.run(app)