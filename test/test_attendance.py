import sys
import os
sys.path.insert(0, os.getcwd()[:len(os.getcwd()) - 4]+"src")
import CRRAttendance

    
def test_swipe_in():
    c = CRRAttendance.open_interface("../res/clientSecret","Node","../res/config.json")
    c.clear_attendence_log()
    c.log_swipe("Lucas")
    assert c.get_active_users()[0][0] == "Lucas"

def test_swipe_out():
    c = CRRAttendance.open_interface("../res/clientSecret","Node","../res/config.json")
    c.clear_attendence_log()
    c.log_swipe("Lucas")
    c.log_swipe("Lucas")
    assert c.get_active_users() == []