#globals defined here
import threading
pool = []
cam = False
img_conn = False
ctrl_conn = False
ctrl_reader = False
pool_lock = threading.Lock()
#captureEvent = threading.Event()
exitEvent = threading.Event()
