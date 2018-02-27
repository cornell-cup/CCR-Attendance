import sys
import os
sys.path.insert(0,os.getcwd()+"/src")
import CCRAttendance
import CCRResources
from RpiRFID import RpiRFID
import signal
import RPi.GPIO as GPIO

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
read = True

def end_read(signal,frame):
    global read
    print "Ctrl+C captured, ending read."
    read = False
    reader.stop()
    GPIO.cleanup()
    exit(0)

signal.signal(signal.SIGINT,end_read)

def main():
    while read:
        print("Looking for card...")
        uid = reader.read_value()
        print("Found card: {0}").format(uid)
        name = raw_input("Name: ")
        db.register_user(name,uid)
	print("Registered User {0} with id {1}").format(name,uid)

main()




