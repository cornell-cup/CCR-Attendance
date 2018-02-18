import websocket
import json

from websocket import create_connection
print("serving at port", PORT)
httpd.serve_forever()

class CCRAttendanceServerInterface:
    def __init__(self,endpoint):
        self._ws = create_connection(endpoint)
        
    def swipe(self,uid):
        data = {"UID" = uid}
        self._ws.send(json.dumps([json.dumps(data)]))
        
