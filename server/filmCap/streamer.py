import threading
import struct
import io
import logging
from time import sleep
import config

class ImageStreamer(threading.Thread):
    def __init__(self, connlock, poollock):
        super(ImageStreamer, self).__init__()
        self.connlock = connlock
        self.poollock = poollock
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.imgflag='s'
        self.start()

    def run(self):
        # This method runs in a separate thread
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                   with self.connlock:
                        send_a_file(self.imgflag, self.stream)
                finally:
                    self.event.clear() # Declare ourselves finished and return$
                    with self.poollock:
                        config.pool.append(self)

#This thread just dumps preview images to the image connection, but also handles requests for shutter speed or gains data
class PreviewThread (threading.Thread):
    def __init__(self, connlock):
        super(PreviewThread, self).__init__()
        self.threadID = 1
        self.name = "PreviewThread"
        self.connlock = connlock
        self.stream = io.BytesIO()

    def run(self):
        logging.info("PreviewThread started")
        cam=config.cam
        #sstest=True
        #i=0
        while not config.exitEvent.is_set():
            self.sendGainsIfNeeded()
            self.sendSSifNeeded()
            if cam.mode == cam.PREVIEWING: # and not self.cam.capturing:  
                logging.debug("Starting Preview Loop")
                for foo in cam.capture_continuous(self.stream, 'jpeg', use_video_port=True):
                    send_a_file('p', self.stream)
                    if cam.mode != cam.PREVIEWING:
                        logging.debug("Preview stopping")
                        config.img_conn.write("t") #to tell server we're done sending
                        config.img_conn.flush()
                        break
                    if config.exitEvent.is_set():
                        break
                    self.sendSSifNeeded()
                    self.sendGainsIfNeeded()
            sleep(1)
        #logging.debug("Preview Thread Sleeping")
        logging.info("Preview Thread Ending")

    def sendGainsIfNeeded(self):
        gains=config.cam.sendgains
        if gains:
            with self.connlock:
                conn=config.img_conn
                r=int(gains[0]*100)
                b=int(gains[1]*100)
                logging.debug("Gain data:"+str(r)+" "+str(b))
                conn.write('g') #to signal this is not image, just color gain data
                conn.write(struct.pack('<L',r))
                conn.write(struct.pack('<L',b))
                conn.flush()
                config.cam.sendgains = False    

    def sendSSifNeeded(self):
        ssflag=config.cam.sendss
        if ssflag:
            with self.connlock:
                conn=config.img_conn
                cam=config.cam
                ss=cam.ss
                again=int(cam.analog_gain*100)
                dgain=int(cam.digital_gain*100)
                conn.write('f') #to signal this is not image, just shutter speed data
                logging.debug("Shutter data: %d %d %d" %(ss,again,dgain))
                conn.write(struct.pack('<L', ss))
                conn.write(struct.pack('<L', again))
                conn.write(struct.pack('<L', dgain))
                conn.flush()
                config.cam.sendss = False

def send_a_file (flag, stream):
    conn=config.img_conn
    conn.write(flag)
    size = stream.tell()
    conn.write(struct.pack('<L', size))
    #logging.debug(flag + str(size))
    conn.flush()
    stream.seek(0)
    conn.write(stream.read())
    stream.seek(0)
    stream.truncate()

