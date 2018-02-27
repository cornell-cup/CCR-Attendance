import sys
import os
sys.path.insert(0,os.getcwd()+"/src")
import CCRAttendance
import CCRResources
import threading
from threading import Lock
import time


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
        
        self._cache = {
                "users" : {
                    "data" : [],
                    "lifetime":60,
                    "last_update":0
                },
                "active_users" : {
                    "data" : [],
                    "lifetime":60,
                    "last_update":0
                },
                "meetings" : {
                    "data" : [],
                    "lifetime":60*24,
                    "last_update":0
                },
                "projects" : {
                    "data" : [],
                    "lifetime":60*24,
                    "last_update":0
                }
        }

        self._running = False
        self._queue_mutex = Lock()
        if with_reader:
            self._reader = RpiRFID()

    def queue_swipe(self,swipe):
        self._queue_mutex.acquire()
        self._swipe_queue.append(swipe)
        self._queue_mutex.release()

    def get_projects(self):
        return self.db.get_projects_list()

    def get_meetings(self):
         return self.db.get_meetings_list()

    def get_swipe(self):
        return self._reader.read_value()

    def get_user_name_swipe(self):
        id = self.get_swipe()
        if not self.cache_entry_expired("users"):
            _, name = self.db.get_name_from_ID(id,self._cache["users"])
            return (id,name)
        else:
            users, name =  self.db.get_name_from_ID(id)
            self.update_cache_entry("users",users)
            return (id,name)

    def _do_swipe_listening_in_job(self):
        self._running = True
        while self._running:
            self.queue_swipe(self.get_user_name_swipe())

    def async_get_user_name_swipe(self,callback):
        self.async_get_swipe(lambda id,name:callback(self.db.get_name_from_ID(id,name)))

    def async_get_swipe(self,callback):
        read_thread = threading.Thread(target=lambda:callback(self.get_swipe()))
        read_thread.start()

    def log_swipe_in(self,id,meeting,team):
        self.db.log_swipe_in(id,meeting,team)

    def log_swipe_out(self,id):
        if not self.cache_entry_expired("active_users"):
            self.db.log_swipe_out(id,self._cache["active_users"])
        else:
            active_users, _ = self.db.log_swipe_out(id)
            self.update_cache_entry("active_users",active_users)

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

    def has_reader(self):
        return with_reader

    def clear_cache(self):
        pass
    
    def cache_entry_expired(self,key):
        return time.time() - self._cache[key]["last_update"] >= self._cache[key]["lifetime"]

    def update_cache_entry(self,key,data):
        self._cache[key]["data"] = data
        self._cache[key]["last_update"] = time.time()