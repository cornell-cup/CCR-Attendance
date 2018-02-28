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
    db.log_swipe_in(123,"Name","Merc","Merc")
    assert int(db.get_active_users()[0]["id"]) == 123

def test_swipe_in_multi():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    db.clear_attendence_log()
    db.log_swipe_in(123,"Name","Merc","Merc")
    db.log_swipe_in(456,"Name","Merc","Merc")
    assert int(db.get_active_users()[0]["id"]) == 123 and int(db.get_active_users()[1]["id"]) == 456

def test_swipe_out():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    db.clear_attendence_log()
    db.log_swipe_in(123,"Name","Merc","Merc")
    db.log_swipe_out(123)
    assert db.get_active_users() == []

def test_timeout():
    db = CCRAttendance.open_db_interface(res("client_secret.json"),"Node",res("db_config.json"))
    db.clear_attendence_log()
    db.log_swipe_in(123,"Name","Merc","Merc")
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

