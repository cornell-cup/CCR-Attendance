import sys
import os
sys.path.insert(0,os.getcwd()+"/src")
import CCRAttendance
import CCRResources
import asyncio
import threading
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

class CCRAttendanceNode:
    def __init__(self):
        self._listeners = []
        # swipes that were sucessfully logged by db, will be added to a queue
        self._swipe_queue = []

    def add_listener(self,listener):
        self._listeners.add(listener)

    def notify_listener_swipe_in(self):
        for listener is self._listeners:
            listener.swipe_in(id)

    def notify_listener_swipe_in(self):
        for listener is self._listeners:
            listener.swipe_out(id)

    def _do_swipe_logging_in_job(self):
        while running:
            id = reader.read_value()                    
            if id is not None:
                res = db.log_swipe(id)
                #if the db update was successful, we add the swipe to the swipe queue to be handled by kivy.
                if res["success"]:
                    self._swipe_queue.append(res)

    def start_swipe_logging_in_job(self):
        t = threading.Thread(target=self._do_sign_in_job)
        t.start()

    # is the swipe queue not empty
    def has_swipe_available(self):
        return len(self._swipe_queue) != 0
    
    # pop a swipe out of the swipe queue
    def pop_swipe(self):
        swipe = self._id_queue[0]
        self._swipe_queue = self._swipe_queue[1:]
        return id
