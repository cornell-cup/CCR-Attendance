import sys
import os
sys.path.insert(0,os.getcwd()+"/src")
import CCRAttendance
import CCRResources
import asyncio
from RpiRFID import RpiRFID

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("client_secret")
    parser.add_argument("application_name")
    parser.add_argument("config_file")
    flags = parser.parse_args()
except ImportError:
    flags = None

CCRResources.populate("res")
db = CCRAttendance.open_db_interface(flags.client_secret,flags.application_name,flags.config_file)
reader = RpiRFID()
loop = asyncio.get_event_loop()
scan_queue = asyncio.Queue(loop=loop)
running = True

class CCRAttendanceNodeListener:
    def swipe_in(self,id):
        raise NotImplementedError("Implement swipe_in")

    def swipe_out(self,id):
        raise NotImplementedError("Implement swipe_out")

class CCRAttendanceNode:
    def __init__(self):
        self._listeners = []

    def add_listener(self,listener):
        self._listeners.add(listener)

    def notify_listener_swipe_in(self):
        for listener is self._listeners:
            listener.swipe_in(id)

    def notify_listener_swipe_in(self):
        for listener is self._listeners:
            listener.swipe_out(id)

    def do_sign_in_job(self):
        while running:
            id = await reader.read_value()                    
            if id is not None:
                resp = db.log_swipe(id)
                if resp["success"]:
                    if resp["direction"] == "IN":
                        self.notify_listener_swipe_in()
                    elif resp["direction"] == "OUT":
                        self.notify_listener_swipe_out()                            
                    else:
                        print "Invalid swipe direction"

