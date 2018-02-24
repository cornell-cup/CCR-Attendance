import sys
import os
sys.path.insert(0, os.getcwd()[:len(os.getcwd()) - 4]+"src")
import CCRResources
from CCRAttendanceNode import CCRAttendanceNode
from CCRResources import res
import time

CCRResources.populate("../res")

def test_swipe_dequeue():
    node = CCRAttendanceNode(res("client_secret.json"),"Node",res("db_config.json"))
    node.queue_swipe({"flag":"test"})
    swipe = node.pop_swipe()
    assert swipe == ({"flag":"test"})

def test_swipe_queue_empty():
    node = CCRAttendanceNode(res("client_secret.json"),"Node",res("db_config.json"))
    node.queue_swipe({"flag":"test"})
    node.pop_swipe()
    assert not node.has_swipe_available()
    
    

