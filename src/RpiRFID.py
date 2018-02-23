import RPi.GPIO as GPIO
from MFRC522 import MFRC522
import time 
import asyncio

rfid_read_sleep = 0.001 # seconds
do_read = True

class RpiRFID:
    def __init__(self):
        self._reader = None

    def init(self):
        self._reader = MFRC522()

    def read_value(self):
        while do_read:
            await asyncio.sleep(rfid_read_sleep)
            (status,_) = self._reader.MFRC522_Request(MFRC522.PICC_REQIDL)

            if status == MFRC522.MI_OK:
                (status,uid) = self._reader.MFRC522_Anticoll()

            if status == MFRC522.MI_OK:    
                return uid

    def stop(self):
        do_read = False
                
            