import time
import RPi.GPIO as GPIO
from timeit import default_timer as timer
import logging
loglevel=logging.DEBUG
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - $(levelname)s - %(message)s')
dir_pin = 18
ms1_pin = 22
ms2_pin = 23
sleep_pin = 27
reset_pin = 15
pulse_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(pulse_pin, GPIO.OUT)
GPIO.setup(ms1_pin, GPIO.OUT)
GPIO.setup(sleep_pin, GPIO.OUT)
GPIO.setup(reset_pin, GPIO.OUT)
dir=False
GPIO.output(dir_pin, dir)
GPIO.output(pulse_pin, False)
GPIO.output(ms1_pin, True)
GPIO.output(sleep_pin, False)
GPIO.output(reset_pin, True)

pulse_freq=500
time.sleep(1)

def pulsetest():
	dir=True
	for freq in [200, 400, 800, 1000]:
		halfpulse=.5/freq
#	for j in range(0,i):
		logging.debug("start")
		for i in range(0,1600):
			GPIO.output(pulse_pin, True)
			time.sleep(halfpulse)
			GPIO.output(pulse_pin, False)
			time.sleep(halfpulse)
		logging.debug("stop")
		dir=not dir
		GPIO.output(dir_pin, dir)
		time.sleep(.5)
#	logging.debug(i)

def pwmtest(i):
	for freq in [200, 400, 800, 1600, 3200]:
		p1 = GPIO.PWM(pulse_pin, freq)
		logging.debug(freq)
		p1.start(10)
		logging.debug('started')
		time.sleep(i)
		logging.debug('stopping')
		p1.stop()
		logging.debug('stopped')
		time.sleep(2)

#time.sleep(2)
#pwmtest(4)
GPIO.output(sleep_pin, True)
#time.sleep(15)
#logging.debug("Sleep off but reset still on")
pulsetest()
GPIO.output(ms1_pin, False)
pulsetest()
GPIO.output(ms1_pin, True)
time.sleep(2)
GPIO.output(sleep_pin, False)

#time.sleep(15)

class fcControl():
	
    def __init__(self):
	pass
	
        #self.light = lightControl(self.light_pin, True)
        #self.redled = lightControl(self.red_pin)
        #self.yellowled = lightControl(self.yellow_pin)
        #self.motor = motorControl(self.fwd_pin, self.rev_pin)
        #self.trigger = trigger(self.trigger_pin)
        #self.motorstate = 0
        #self.smart_motor = False
        #self.smart_headroom = 25
        #self.triggertime = 0
        #self.qlen = 5
        #self.triggertimes = collections.deque([],self.qlen)
        #self.phototimes = collections.deque([],self.qlen)
        

    def light_on(self):
        self.light.on()
    def light_off(self):
        self.light.off()
    def red_on(self):
        self.redled.on()
    def red_off(self):
        self.redled.off()
    def yellow_on(self):
        self.yellowled.on()
    def yellow_off(self):
        self.yellowled.off()
    def yellow_is_on(self):
        return GPIO.input(self.yellow_pin)

    def cleanup(self):
        print "Cleanup"
        self.light.off()
        self.redled.off()
        self.yellowled.off()
        self.motor.stop()
        GPIO.cleanup()

    def motor_fwd(self, speed=False):
        if (not speed):
            speed = self.speed
        self.motor.fwd(speed)
        self.motorstate = 1
    def motor_rev(self, speed=False):
        if (not speed):
            speed = self.speed
        self.motor.rev(speed)
        self.motorstate = -1
    def motor_stop(self):
        self.motor.stop()
        self.motorstate = 0
        self.triggertimes.clear()
        self.phototimes.clear()

    def motor_set_speed(self, speed):
        speed=min(speed,100)
        self.speed = speed
        logging.debug("speed:"+str(speed))
        if self.motorstate==1:
            self.motor_fwd(speed)
        if self.motorstate==2:
            self.motor_fwd(speed)

    def start_photo(self):
        ttimes=self.triggertimes
        ptimes=self.phototimes
        trig=self.triggertime
        qlen=self.qlen
        headroom=self.smart_headroom/100.0
        start=timer()
        if trig:
            ttimes.appendleft(start-trig)
        self.triggertime = start
        #if we have a full set of intervals, calculate average and adjust motor
        if len(ttimes) == qlen and len(ptimes) == qlen:
            tavg=sum(ttimes)/qlen
            pavg=sum(ptimes)/qlen
            avgGap=tavg-pavg
            lastGap=ttimes[0]-ptimes[0]
            neededGap=tavg*headroom
            diff=avgGap-neededGap
            diffpct=diff/headroom  #this how far off the headroom we are, as a fraction of that headroom
            logging.debug(str(tavg)+" "+str(pavg)+" "+str(lastGap)+" "+str(diffpct))
            if lastGap<neededGap*.8 or diffpct<-.1:
                logging.debug("Way Fast")
                self.motor_set_speed(self.speed-7)  #if the last frame or avg is way off 
            elif lastGap<neededGap*.9 or diffpct<0:
                logging.debug("Fast")
                self.motor_set_speed(self.speed-1) #if we're just barely under required gap
            elif diffpct>.5:  #if we're well over, speed up aggressively
                logging.debug("Way Slow")
                self.motor_set_speed(self.speed+2)
            elif diffpct>.2: #if we're close, tweak it
                logging.debug("Slow")
                self.motor_set_speed(self.speed+1)
            
    def end_photo(self):
        newtime = timer()
        phototime = newtime - self.triggertime
        self.phototimes.appendleft(phototime)
        
    

	
class lightControl:
    def __init__(self, pin, reversed=False):
	self.pin = pin
	self.reversed = reversed
	GPIO.setup(pin, GPIO.OUT)
	self.off()

    def on(self):
	GPIO.output( self.pin, not(self.reversed) )

    def off(self):
	GPIO.output( self.pin, self.reversed )

class motorControl:
    pulse_freq = 500
    def __init__(self, fwdpin, revpin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(pulse_pin, GPIO.OUT)
        GPIO.setup(ms1_pin, GPIO.OUT)
        GPIO.setup(sleep_pin, GPIO.OUT)
        GPIO.setup(reset_pin, GPIO.OUT)

        GPIO.output(revpin, False)
        self.p1 = GPIO.PWM(fwdpin, self.pulse_freq)
        self.p2 = GPIO.PWM(revpin, self.pulse_freq)

    def fwd(self, speed):
        self.p2.stop()
        self.p1.start(int(speed))
    def rev(self, speed):
        self.p1.stop() #ChangeDutyCycle(0)
        self.p2.start(int(speed))
    def stop(self):
        self.p1.stop(0)
        self.p2.stop(0)

class trigger:
    def __init__(self, triggerpin):
	GPIO.setup(triggerpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	self.pin = triggerpin

    

