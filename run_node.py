import sys
import os
sys.path.insert(0,os.getcwd()+"/src")
import CCRAttendance
import CCRResources
import asyncio
from RpiRFID import RpiRFID

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

api_key = "test_key"
CCRResources.populate("res")
interface = CCRAttendance.open_db_interface(flags.client_secret,flags.application_name,flags.config_file)
server = CRRAttendance.connect_server(flags.endpoint,api_key)
reader = RpiRFID()
loop = asyncio.get_event_loop()
scan_queue = asyncio.Queue(loop=loop)
running = True
rfid_read_hz = 100.0

def sign_in_job():
    while running:
        id = reader.read_value()                    
        if id is not None:
            server.swiped(id)

if __name__ == 'main':
    #TODO: Read RFID, Update Sheets, etc. Probably should be done Asynchronously

