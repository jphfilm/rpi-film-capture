#!/usr/bin/python
import socket
import time
import picamera
import threading        #should probably change threads to processes. Sometime.
import multiprocessing  #using processes instead of threads for frame advance.
import filmCap
from time import sleep
import RPi.GPIO as GPIO
from filmCap import config
from filmCap import codes

import logging
loglevel = logging.DEBUG #SET TO [CRITICAL|ERROR|WARNING|INFO|DEBUG]
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#FOR SERVER-BASED EXPOSURE CONTROL
imgbrightness = 100
imgbrightness2 = 80
brt_max_single = 150
brt_max_double = 170
brt_min_single = 70
brt_min_double = 50

missed_frames = 0
img_format = 'jpeg'  #Works with other formats, but clarge sizes make it much slower.
jpeg_quality = 95

auto_advance = False #this determines whether we advance after each photo
                     #turned on/off by commands from client   
readerExitEvent = threading.Event()
cap_event = multiprocessing.Event()
exit_event = multiprocessing.Event()

def setupConns(img_socket, ctrl_socket):
    global ctrl_reader, readerExitEvent
    readerExitEvent.clear()
    logging.info("Waiting for client connection...")
    config.img_conn = img_socket.accept()[0].makefile('wb')
    config.ctrl_conn = ctrl_socket.accept()[0].makefile('rb')
    logging.info("Client Connections Established")
    ctrl_reader=filmCap.NonBlockingStreamReader(config.ctrl_conn, readerExitEvent)

def releaseClient():
    global img_socket, ctrl_socket, ctrl_reader, readerExitEvent
    readerExitEvent.set()
    ctrl_reader.thr.join()
    config.img_conn.flush()
    config.img_conn.close()
    config.ctrl_conn.flush()
    config.ctrl_conn.close()
    logging.info("Client connections released")
    setupConns(img_socket, ctrl_socket) #wait for new connection from client

def sendquit():
    config.img_conn.write("t") #to tell server we're done sending
    config.img_conn.flush()

def processCmd(cmdstr):
    global fc, auto_advance
    cam=config.cam
    c=filmCap.codes
    if not cmdstr:
        logging.debug("Empty Command String")
        return 0
    cmdstr=cmdstr.replace("\n", "")
    logging.debug(cmdstr)
    cmd=cmdstr[0]
    setting=cmdstr[1:]

    #preview settings
    if cmd == c.MOTOR_FWD:
        fc.motor_fwd(30)
    elif cmd == c.MOTOR_REV:
        fc.motor_rev(30)
    elif cmd == c.MOTOR_FFD:
        fc.motor_fwd(100)
    elif cmd == c.MOTOR_FREV:
        fc.motor_rev(100)
    elif cmd == c.MOTOR_STOP:
        fc.motor_stop()
    elif cmd == c.LIGHT_OFF:
        fc.light_off()
    elif cmd == c.LIGHT_ON:
        fc.light_on()
    elif cmd == c.PREVIEW_ON:
        cam.mode = cam.PREVIEWING
    elif cmd ==  c.PREVIEW_OFF:
        cam.mode = cam.OFF
    elif cmd == c.AUTOEXP_ON:
        cam.exposure_mode = "auto"
    elif cmd ==  c.AUTOEXP_OFF:
        cam.exposure_mode = "off"
        
    elif cmd == c.SETX:
        cam.setx(int(setting))
    elif cmd == c.SETY:
        cam.sety(int(setting))
    elif cmd == c.SETZ:
        cam.setz(int(setting))
    # Color Settings
    elif cmd == c.GAIN_RED:
        cam.set_yuv(0,float(setting)/100)
    elif cmd == c.GAIN_BLUE:
        cam.set_yuv(1,float(setting)/100)
    elif cmd == c.BRIGHTNESS:
        cam.brightness = int(setting)
    elif cmd == c.EXP_COMP:
        cam.exposure_compensation = int(setting)
    elif cmd == c.SATURATION:
        cam.saturation = int(setting)
    elif cmd == c.CONTRAST:
        cam.contrast = int(setting)
    elif cmd ==  c.FIX_GAINS:
        cam.fixAndSendGains()
    elif cmd == c.AWB_MODE:
        cam.awb_mode = setting

    #Advanced controls
    elif cmd == c.DRC:
        cam.drc_strength = setting
    elif cmd == c.HFLIP_ON:
        cam.hflip = True
    elif cmd == c.HFLIP_OFF:
        cam.hflip = False
    elif cmd == c.VFLIP_ON:
        cam.vflip = True
    elif cmd == c.VFLIP_OFF:
        cam.vflip = False
    elif cmd == c.BW_ON:
        cam.color_effects = (128,128)
    elif cmd == c.BW_OFF:
        cam.color_effects = None
    elif cmd == c.SHARPNESS:
        cam.sharpness = int(setting)
    elif cmd == c.VID_PORT_ON:
        cam.vidcap = True
    elif cmd == c.VID_PORT_OFF:
        cam.vidcap = False
    elif cmd == c.SET_SIZE:
        cam.setResize(int(setting))

    #Capture settings for tab switch
    elif cmd == c.CAPTURE_ON:
        if cam.mode != cam.CAPTURING:
            fc.light_on()
            cam.startCaptureMode()
            take_a_photo(0)
    elif cmd == c.CAPTURE_OFF:
        if cam.mode == cam.CAPTURING:
            cam.startPreviewMode()

    #Capture settings
    elif cmd == c.BRACKETING_SHOTS:
        cam.bracketing=int(setting)
        cam.sendss=True
    elif cmd == c.BRACKETING_STOPS:
        cam.stops = float(setting)
        cam.sendss=True
    elif cmd == c.FIX_EXPOSURE:
        cam.setExposure()
        take_a_photo(0) #take a single photo and stream it.
    elif cmd == c.SS_SLOWER:
        cam.ss = int(cam.ss * 1.23)
        cam.shutter_speed = int(cam.ss)
        cam.sendss = True
    elif cmd == c.SS_FASTER:
        cam.ss = int(cam.ss * .81)
        cam.shutter_speed = int(cam.ss)
        cam.sendss = True
    elif cmd == c.QUIT:
        config.exitEvent.set()
    elif cmd == c.CLIENT_QUIT:
        cam.mode = cam.OFF
        sendquit()
        time.sleep(2)
        releaseClient()
    elif cmd == c.TEST_PHOTO:
        take_a_photo(0) #take a single photo and stream it.
        cam.sendss = True
    elif cmd == c.START_CAPTURE:
        auto_advance=True
        fc.motor_wake()
        take_a_photo(0)
    elif cmd == c.STOP_CAPTURE:
        auto_advance=False
        #fc.motor_sleep()
    elif cmd == c.CAP_FRAME_ADV:
        cam.mode=cam.OFF
        num=int(setting) if setting else 1
        fc.motor.fwdFrame(num)  
        cam.mode=cam.CAPTURING
        take_a_photo(0) #take a single photo and stream it.
    elif cmd == c.CAP_FRAME_REV:
        cam.mode=cam.OFF
        auto_advance = False
        num=int(setting) if setting else 1
        fc.motor.revFrame(num)  
        cam.mode=cam.CAPTURING
        take_a_photo(0) #take a single photo and stream it.
    elif cmd == c.SET_MOTOR_SPEED:
        fc.motor_set_speed(int(setting))

    #smart capture settings
    elif cmd -- '^':
        if setting:
            fc.smart_motor = True
            fc.smart_headroom = setting
        else:
            fc.smart_motor = False

def camera_busy():
    global fc #, missed_frames, cam_lock
    #used to have logic to ensure cam coultn't be triggered before it was finished
    #with previous photo.  Using stepper motors should prevent the need for this
    fc.yellow_on()

def camera_free():
    global fc #, cam_lock
    fc.yellow_off()

def take_a_photo(channel):  #callback triggered by frame advance setting GPIO pin
    global fc, auto_advance, cap_event
    cam = config.cam
    sleep(0.05)  #wait before checking status of trigger, to avoid false triggers
    logging.debug("Trigger "+str(GPIO.input(fc.trigger_pin))+str(cam.mode))
    if (((channel == 0) or (GPIO.input(fc.trigger_pin) == 1)) and cam.mode==cam.CAPTURING):  #only take this photo if we're in capture mode
        logging.debug("Trigger Valid")
        #if channel!=0: #photo hasn't been triggered, so we're not monitoring it
        camera_busy()
        i=1
        if channel == 0:  #this signifies a non-triggered photo, so we need to manually set the initial shutter speed
            cam.shutter_speed = bracketSS(cam.stops, i, cam.bracketing, cam.ss)
            sleep(1.5/cam.framerate)
        while i<= cam.bracketing:
            while not len(config.pool):  #if we don't have enough processors for the next photo (maybe because of network congestion or a busy client)
                sleep(1)                #the we just wait until we do.  This should be rare, but it will happen
            logging.debug("Photo "+str(i)+" taken "+str(cam.shutter_speed)+" "+str(cam.analog_gain)+" "+str(cam.digital_gain))
            imgflag = 's' if cam.bracketing==1 else 'a' if i<cam.bracketing else 'b'
            take_and_queue_photo(imgflag)
            logging.debug("Photo "+imgflag+" taken "+str(cam.shutter_speed)+" "+str(cam.analog_gain)+" "+str(cam.digital_gain))
            #trying AFTER photo, to avoid delaying at beginning.
            nextshot=i+1 if i<cam.bracketing else 1
            cam.shutter_speed = bracketSS(cam.stops, nextshot, cam.bracketing, cam.ss)
            #below line is really important! Without sufficient delay, camera won't use new shutter speed
            #on next photo.  Only necessary when using video port.
            if i< cam.bracketing:
                sleep(1.3/cam.framerate)#try giving camera time to register new shutter speed
            i+=1
        camera_free()
        if auto_advance:
            cap_event.set()  #send the signal to the motor winder
        logging.debug("Photo taken")

def bracketSS(stops, shot, bkt, ss):   #determine shutter speed for arbitrary number of bracketed shots, at arbitrary spread of stops
    if bkt == 1:
        return ss
    else:
        adj = (float(shot-1)/float(bkt-1)*2)-1  #should provide an evently spaced range of values between -1 and 1
        #so if bkt = 1, it's [-1,1] if 3, it's [-1,0,1], if 4 it's [-1,-1/3,1/3,1], etc. 
        return int(ss*1.41**(adj*stops))

def take_and_queue_photo(imgflag):
    global auto_advance
    cam=config.cam
    processor=None
    while not processor:
        with config.pool_lock:
            if config.pool:
                processor = config.pool.pop()
        if processor:
            #logging.debug("Got processor")
            stream=processor.stream
            cam.capture(stream, img_format, quality=jpeg_quality, use_video_port = cam.vidcap, resize=cam.capsize)
            #logging.debug("got photo")
            processor.imgflag = imgflag
            processor.event.set()   #start the thread which streams the photo
            #logging.debug("Set Event")
            return 0
        else:   #When the pool is starved, wait a while for it to refill
            logging.warning("No Processors available in pool - stopping capture")
            auto_advance = False
            time.sleep(1)

###########MAIN LOOP BELOW #######################
logging.info("Starting")
#Set up sockets and connections
img_socket = socket.socket()
img_socket.bind(('0.0.0.0', 8000))
img_socket.listen(0)
ctrl_socket = socket.socket()
ctrl_socket.bind(('0.0.0.0', 8001))
ctrl_socket.listen(0)

cam_lock = threading.Lock()
#SETUP LOsCKS FOR POOL OF THREADS USED BY IMAGE STREAMING THREADS
connection_lock = threading.Lock()
config.pool = [filmCap.ImageStreamer(connection_lock, config.pool_lock) for i in range(5)]
#We use separate threads to stream captured images so that the
# camera will never miss a shot while waiting for an image to
#stream over the network. It's complex, but allows for faster
#capture rates with fewer missed/blurred frames
#Trying with 5 threads to support extreme bracketing
previewthread = filmCap.PreviewThread(connection_lock)
driverprocess = filmCap.MotorDriver(cap_event, exit_event)
driverprocess.start()


GPIO.setwarnings(False)  #to suppress irrelevant messages

try:
    config.cam= filmCap.fcCamera()
    fc = filmCap.fcControl()
    logging.debug("Control Object Created")
    #add callback for triggering pictures
    GPIO.add_event_detect(fc.trigger_pin, GPIO.RISING, callback=take_a_photo, bouncetime = 25)
    logging.debug("GPIO Setup Complete")


    setupConns(img_socket, ctrl_socket)
    previewthread.start()
    logging.debug("previewthread started")

    while not config.exitEvent.is_set():
        data=ctrl_reader.readline(1)
        if data:
            processCmd(data)
    if config.exitEvent.is_set():
        logging.debug("Exit Event Set")
except KeyboardInterrupt as inst:#Exception as inst:
    logging.debug("Kbd Interrupt")
    logging.debug(type(inst))    # the exception instance
    #pass
finally:
    logging.debug("Exiting....")
    config.exitEvent.set()  #this is the threading.event to stop the preview & streamer threads
    exit_event.set()        #this is the processing.Event to stop the motor
    while config.pool:      #terminate the pool of image streaming threads
        streamer = config.pool.pop()
        streamer.terminated = True
        streamer.join()
    if previewthread.isAlive():
        previewthread.join()
    driverprocess.join()
    #Close the connections
    if config.img_conn:
        config.img_conn.close()
    if config.ctrl_conn:
        config.ctrl_conn.close()
    if img_socket:
        img_socket.close()
    if ctrl_socket:
        ctrl_socket.close()
    fc.cleanup()    #Stop motor, light off, release GPIO pins
    logging.info("All sockets closed - exited")
