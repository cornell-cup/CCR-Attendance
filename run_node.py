import sys
import os
sys.path.insert(0,os.getcwd()+"../src")
import CCRAttendance
import CCRResources

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("client_secret")
    parser.add_argument("application_name")
    parser.add_argument("config_file")
    flags = parser.parse_args()
except ImportError:
    flags = None

if __name__ == 'main':
    CCRAttendance.populate("res")
    CCRAttendance.make_interface(flags.client_secret,flags.application_name,flags.config_file)
    #TODO: Read RFID, Update Sheets, etc. Probably should be done Asynchronously