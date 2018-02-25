import sys
import os
sys.path.insert(0,os.getcwd()+"/src")
import CCRAttendance
import CCRResources
import threading
from threading import Lock

with_reader = False

try:
    from RpiRFID import RpiRFID
    with_reader = True
except ImportError:
    print("Not running on RPI")

class CCRAttendanceNode:
    def __init__(self,client_secret,application_name,config_file):
        self._listeners = []
        # swipes that were sucessfully logged by db, will be added to a queue
        self._swipe_queue = []
        self.db = CCRAttendance.open_db_interface(client_secret,application_name,config_file)
        self._cache = {}
        self._running = False
        self._queue_mutex = Lock()
        if with_reader:
            self._reader = RpiRFID()

    def queue_swipe(self,swipe):
        self._queue_mutex.acquire()
        self._swipe_queue.append(swipe)
        self._queue_mutex.release()

    def get_swipe(self):
        return self._reader.read_value()

    def get_user_swipe(self):
        id = self.get_swipe()
        if self.db.validate_uid(id):
            return id

    def _do_swipe_listening_in_job(self):
        while self._running:
            return self.get_user_swipe()

    def log_swipe_in(self,id,meeting,team):
        self.db.log_swipe_in(id,meeting,team)

    def log_swipe_out(self,id):
        self.db.log_swipe_out(id)

    def user_is_swiped_in(self,id): 
        return id in self.db.get_active_users()

    def start_swipe_logging_job(self):
        t = threading.Thread(target=self._do_swipe_listening_in_job)
        t.start()

    def stop_swipe_logging_job(self):
        self._running = False
    # is the swipe queue not empty
    def has_swipe_available(self):
        return len(self._swipe_queue) != 0
    
    # pop a swipe out of the swipe queue
    def pop_swipe(self):
        self._queue_mutex.acquire()
        swipe = self._swipe_queue[0]
        self._swipe_queue = self._swipe_queue[1:]
        self._queue_mutex.release()
        return swipe

    def clear_cache(self):
        pass