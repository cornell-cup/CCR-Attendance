import sys
import os
sys.path.insert(0,os.getcwd()+"/src")
from RpiRFID import RpiRFID
import CCRAttendanceimport signal


try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("client_secret")
    parser.add_argument("application_name")
    parser.add_argument("config_file")
    parser.add_argument("endpoint")
    flags = parser.parse_args()
except ImportError:
    flags = None

CCRResources.populate("res")
interface = CCRAttendance.open_db_interface(flags.client_secret,flags.application_name,flags.config_file)
signal.signal(signal.SIGINT, end_read)

read = True

def end_read(signal,frame):
    global read
    print "Ctrl+C captured, ending read."
    read = False
    GPIO.cleanup()

def main():
    while read:
        reader = RpiRFID()
        print("Looking for card...")
        uid = reader.read()
        print("Found card: %i",uid)
        name = raw_input("Name: ")
        interface.register_user(name,uid)






