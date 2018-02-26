import sys
import os
sys.path.append("../src")
import CCRAttendance
import CCRResources
from CCRResources import res

CCRResources.populate("../res")

def test_swipe_in():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    db.clear_attendence_log()
    db.log_swipe_in("Lucas","Merc","Merc")
    assert db.get_active_users()[0]["user"] == "Lucas"

def test_swipe_in_multi():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    db.clear_attendence_log()
    db.log_swipe_in("Lucas","Merc","Merc")
    db.log_swipe_in("Lucas2","Merc","Merv")
    assert db.get_active_users()[0]["user"] == "Lucas" and db.get_active_users()[1]["user"] == "Lucas2"

def test_swipe_out():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    db.clear_attendence_log()
    db.log_swipe_in("Lucas","Merc","Merc")
    db.log_swipe_out("Lucas")
    assert db.get_active_users() == []

def test_timeout():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    db.clear_attendence_log()
    db.log_swipe_in("Lucas","Merc","Merc")
    db.log_timeout(2)
    assert db.get_active_users() == []

def test_projects_list():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    projects = db.get_projects_list()
    assert projects == ["Minibot","Vision","Merc"]

def test_projects_list():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    projects = db.get_projects_list()
    assert projects == ["Minibot","Vision","Merc"]

def test_meetings_list():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    projects = db.get_meetings_list()
    assert projects == ["Dave","Saturday Work"]

