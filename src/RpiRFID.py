import MFRC522
import time

rfid_read_sleep = 0.5  # seconds


class RpiRFID:
    def __init__(self):
        self._reader = MFRC522.MFRC522()
        self._do_read = True

    def read_value(self):
        while self._do_read:
            time.sleep(rfid_read_sleep)
            (status, _) = self._reader.MFRC522_Request(self._reader.PICC_REQIDL)

            if status == MFRC522.MFRC522.MI_OK:
                (status,uid) = self._reader.MFRC522_Anticoll()
            uid_int = 0
            if status == MFRC522.MFRC522.MI_OK:    
                for byte in uid:
                    uid_int = uid_int << 8 | byte
                return uid_int

    def stop(self):
        self._do_read = False
