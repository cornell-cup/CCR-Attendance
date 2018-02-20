import websocket
import json
from websocket import create_connection
import requests

scanner_route = "/scanners/"

class CCRAttendanceServerInterface:
    def __init__(self,endpoint,key):
        self._endpoint = endpoint
        self._key = key

    def swipe(self,uid):
        response = requests.post(self._endpoint + scanner_route + self._key "/" + uid, data = None).json()
        return response["success"]
    

        
