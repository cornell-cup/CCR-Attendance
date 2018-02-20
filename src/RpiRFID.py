import RPi.GPIO as GPIO
import MFRC522

rfid_read_sleep = 1.0
do_read = True

class RpiRFID:
    def __init__(self):
        self._reader = None

    def init(self):
        self._reader = MFRC522.MFRC522()

    def read_value(self):
        while do_read:
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            if status == MIFAREReader.MI_OK:
                (status,uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:    
                return uid

    def stop():
        do_read = False
                
            