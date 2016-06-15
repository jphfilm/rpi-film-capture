import collections

server_ip = "raspberrypi.local"
app = False
test_mode = False
exitFlag = False  
prevOn = False
captureOn = False
frame_limit = 3500
frame_number = 1
frame_start=1
blend = False
blendStops = 1.0
wait_for_test = False
ctrl_conn = False
capture_speed = 70
#for saving files
default_folder = "/storage/Films/"
folder = "."
initfile="startup.ini"
brightProcess=True

last4prev=None
last4init=None
prevFrames=None
initFrames=None

#camera defaults
#bgmin = 50					#Affects the sliders for adjusting color gain
#bgmax = 350
#bgdefault = 200
#rgmin = 50
#rgmax = 200
#rgdefault = 100
#sharpnessdefault = -100		#Films with prominent grain (much 8mm) benefit from lowest possible sharpness

#experimental, for auto-adjusting brightness.
def brightnessInit(prev, lastprev, init, lastinit):
	global last4prev,last4init,prevFrames,initFrames
	#sets up lists we'll use to track brightness
	last4prev=collections.deque([],lastprev)
	last4init=collections.deque([],lastinit)
	prevFrames=collections.deque([],prev)
	initFrames=collections.deque([],init)

imgWinTitle = "Preview"  	#Can be anything
imgWinWidth = 1296 #1/2 the max resolution of the pi camera. Changing does not affect capture size.
imgWinX = 326 #1/2 the max resolution of the pi camera. Changing does not affect capture size.
imgWinHeight= 944
imgWinY= 0

