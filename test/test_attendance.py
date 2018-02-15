import sys
import os
sys.path.insert(0, os.getcwd()[:len(os.getcwd()) - 4]+"src")
import CCRAttendance
import CCRResources
from CCRResources import res

CCRResources.populate("../res")

def test_swipe_in():
    c = CCRAttendance.open_interface(res("client_secret.json"),"Node",res("config.json"))
    c.clear_attendence_log()
    c.log_swipe("Lucas")
    assert c.get_active_users()[0][0] == "Lucas"

def test_swipe_in_multi():
    c = CCRAttendance.open_interface(res("client_secret.json"),"Node",res("config.json"))
    c.clear_attendence_log()
    c.log_swipe("Lucas")
    c.log_swipe("Lucas2")
    assert c.get_active_users()[0][0] == "Lucas" and c.get_active_users()[1][0] == "Lucas2"

def test_swipe_out():
    c = CCRAttendance.open_interface(res("client_secret.json"),"Node",res("config.json"))
    c.clear_attendence_log()
    c.log_swipe("Lucas")
    c.log_swipe("Lucas")
    assert c.get_active_users() == []

def test_timeout():
    c = CCRAttendance.open_interface(res("client_secret.json"),"Node",res("config.json"))
    c.clear_attendence_log()
    c.log_swipe("Lucas")
    c.log_timeout(2)
    assert c.get_active_users() == []

