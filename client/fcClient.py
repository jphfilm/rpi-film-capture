#!/usr/bin/python
import io
import socket
from time import sleep
import sys
import logging
#our own modules:
import config #cross-module globals defined here
from fcConfig import fcConfigParser	#class to store and retrieve settings
from fcDialog import fcDialog		#class defining our main window
from fcImgThread import imgThread	#class and supporting functions supporting image reading
from PyQt4.QtGui import QApplication

def setup_conns(image_socket, control_socket): #sets up 2 connections; one for sending control sequences and one for receiving image data
	image_socket.connect((config.server_ip, 8000))
	control_socket.connect((config.server_ip, 8001))
	img_conn = image_socket.makefile('wb')
	ctrl_conn = control_socket.makefile('wb')
	logging.debug("All Conns Established")
	return (img_conn,ctrl_conn)

if __name__ == "__main__":
	loglevel = logging.DEBUG  #SET TO [CRITICAL|ERROR|WARNING|INFO|DEBUG]
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
	if (len(sys.argv)>1 and sys.argv[1] == 'test'):
		config.test_mode = True
		logging.debug("Test mode="+str(config.test_mode))
	app = QApplication(sys.argv)
	win = fcDialog()
	win.config = fcConfigParser()
	win.show()
	logging.debug("Win Shown")
	#establish thread to listen for images
	if not config.test_mode:
		image_socket = socket.socket()
		control_socket = socket.socket()
		(img_conn, ctrl_conn)=setup_conns(image_socket, control_socket)
		config.ctrl_conn = ctrl_conn
		imgthread = imgThread(img_conn, app)
		win.setupThreadingUpdates(imgthread) #sets up slots to allow image thread to update UI		
		imgthread.start()
		logging.debug("Imgthread started")
		#win.loadConfigFile(config.initfile) #load initial config
		sleep(2)
		#setup capture mode and take first pic
		win.getFirstImg()
	rtnVal=app.exec_()
	logging.debug("Window Closed")
	config.exitFlag=True
	if not config.test_mode:		
		imgthread.wait() #was .join()
		logging.debug("Imgthread quit")
		ctrl_conn.close()
		logging.debug("All Conns Closed")
		#sockets closed
		image_socket.close()
		control_socket.close()
		logging.debug("All Sockets Closed - Exiting")
	sys.exit(rtnVal)
