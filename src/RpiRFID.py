rfid_read_sleep = 1.0
do_read = true

class RpiRFID:
    def __init__(self,spi_port):
        self._reader = None

    def init(self):
        signal.signal(signal.SIGINT, end_read)
        self._reader = MFRC522.MFRC522()

    def read_value()
        while do_read:
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            if status == MIFAREReader.MI_OK:
                (status,uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:    
                return uid

    def stop():
        do_read = False
                
            