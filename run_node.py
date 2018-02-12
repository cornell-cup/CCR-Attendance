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
    flags = parser.parse_args()
except ImportError:
    flags = None


CCRResources.populate("res")
interface = CCRAttendance.make_interface(flags.client_secret,flags.application_name,flags.config_file)
reader = RpiRFID(0)
loop = asyncio.get_event_loop()
scan_queue = asyncio.Queue(loop=loop)
running = True
rfid_read_hz = 100.0

async def rfid_read_job():
    while running:
        id = await reader.read_value() #This should be asyncronous. 
                                       #Have a while to the reading till be get something meaningful and a async sleep
        if id is not None:
            interface.log_swipe(id)
            

if __name__ == 'main':
    #TODO: Read RFID, Update Sheets, etc. Probably should be done Asynchronously

