import picamera
from time import sleep
import logging
import config
#from streamer import CaptureThread
class fcCamera(picamera.PiCamera):
    OFF = 0
    PREVIEWING = 1
    CAPTURING = 2
    res_preview = (1296, 972)
    res_capture = (2592, 1944)
    resolutions = [(2592,1944),(1600,1200),(1440,1080),(1296,972),(1024,768),(800,600)]
    capsize=resolutions[0]
    default_framerate=15
    sendss=False
    
    def __init__(self):
        #logging.debug("Cam init begins")
        super(fcCamera, self).__init__()        
        self.setDefaults()
        #logging.debug("iso"+str(self.iso))
        ##sleep(2)
        #self.awb_mode="off"
        #config.cam.stop_preview()
        #self.exposure_mode = "off"
        ##logging.debug("res changed")
        self.exposure_mode = 'auto'   #let cam adjust exposure for previews
        #self.shutter_speed = 0
        #sleep(2)
        logging.debug("Cam Initialized")
        #self.awb_mode='off'


    def setDefaults(self):
        #sets camera settings to match that of client on startup.  Set on start of server program and when waiting for client connection
        self.mode=self.OFF
        self.vidcap = True #Change this here or dynamically if we want to capture from still port (slower)
        self.bracketing = 1
        self.stops = 1.5
        self.iso = 100
        self.ss = 10000 #where we hold a nominal shutter speed, to be changed every frame when bracketing exposures
        self.resolution = self.res_preview #half resolution for preview images
        self.prev_on = False
        self.sendgains = False  #flag to trigger sending of shutter speed
        self.framerate=15
        self.exposure_mode = "auto"
        self.awb_mode = 'auto' #should already be off but just in case

    def setResize(self, num):
        self.capsize=self.resolutions[num]
        #self.resolution=self.resolutions[num]
        #self.res_capture=self.resolutions[num]
        #logging.debug("Newres"+str(self.resolution))
        
    def startPreviewMode(self):
        self.mode = self.OFF
        #config.captureEvent.set()  #allows capture thread to stop waiting and exit
        sleep(1)
        logging.debug("Switching to prev mode")
        self.resolution = self.res_preview #half resolution for preview images
        print "res changed"
        #self.exposure_mode = 'auto'   #let cam adjust exposure for previews
        self.shutter_speed = 0
        sleep(1)
        print "exp mode set"
        #self.awb_mode='off'
        self.mode = self.PREVIEWING
        print "finished"

    def startCaptureMode(self):
        self.mode = self.OFF   #Other threads won't mess w/ cam while changing mode
        sleep(1)    #To wait for previewer thread to finish
        logging.debug("Starting Capture mode")
        self.resolution = self.res_capture
        #self.setExposure()
        self.mode = self.CAPTURING
        self.ss=self.exposure_speed
        self.sendss=True
        #config.capThread = CaptureThread(config.pool_lock, config.captureEvent)
        #config.capThread.start()  #capThread used by abandoned capture_continuous effort
        #self.sendss = True  #flag to trigger sending of shutter speed
        logging.debug("StartCaptureMode complete")

    def setx(self,val):
        (x,y,w,h) = self.zoom
        x=max(0,float(val)/1000-w/2)
        self.zoom=(x,y,w,h)
    def sety(self,val):
        (x,y,w,h) = self.zoom
        y=max(0,float(val)/1000-h/2)
        self.zoom=(x,y,w,h) 
    def setz(self,val):
        (x,y,w,h) = self.zoom
        z=float(val)/1000
        x=max(0,x+w/2-z/2)
        y=max(0,y+h/2-z/2)
        self.zoom=(x,y,z,z)

    def set_yuv(self, idx, value):
        (rg,bg)=self.awb_gains
        if (idx==0):
            rg=value
        if (idx==1):
            bg=value
        self.awb_gains = (rg,bg)

    def fixAndSendGains(self):
        gains = self.awb_gains
        self.awb_mode = 'off'
        self.awb_gains = gains
        self.sendgains = gains
        logging.debug(gains)

    def setExposure(self):
        self.start_preview()  #NEED TO START PREVIEW BEFORE SETTING THIS!        
        #this temporarily sets a higher framerate, while we fix gains,
        #so that longer bracked exposures won't try to set an exposure 
        #time (shutter_speed) higher than that allowable by the framerate
        self.iso = 0  #lets try this
        
        bracket_adj_factor = 2**(self.stops/2.0)
        #set the framerate based on the bracketing settings
        self.framerate = int(self.default_framerate*bracket_adj_factor)

        #set exposure mode to auto and shutter speed to 0 to allow gains to set
        self.exposure_mode = 'auto'
        self.shutter_speed = 0 #allows it to be set automatically
#        self.shutter_speed = self.exposure_speed
        self.awb_mode = 'off' #should already be off but just in case
        #give camera time to adjust
        sleep(2)
        logging.debug("Setting exposure - awb off"+str(self.exposure_speed))
        logging.debug(str(self.framerate)+"FPS "+str(self.analog_gain)+" "+str(self.digital_gain))
        self.exposure_mode = 'off'  #to fix gains
        self.ss= self.exposure_speed #save it to variable
        self.shutter_speed = self.ss
        logging.debug("ss="+str(self.exposure_speed))
        self.stop_preview()
        self.sendss = True
        
        #then change the framerate BACK
        self.framerate = self.default_framerate

