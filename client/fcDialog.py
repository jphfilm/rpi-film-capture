from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from time import sleep
import os
import logging
#our own files below
import config
from codes import *
from fcClientgui import *		#Our main dialog class, created in QT Designer 
		#and translated to python via "pyuic4 fcClientgui.ui > fcClientgui.py" 

colors = ('b','g','r')	#used by histogram plotter

def sendCtrl(cmd):  #used whenever we send a control sequence to server
	logging.debug("CTRL: " + cmd)
	if not config.test_mode:
		config.ctrl_conn.write(cmd+"\n")
		config.ctrl_conn.flush()

def adj_for_size(pixcount, px): #used by histogram calculation
	return "{0:.2f}".format(float(pixcount/px*100))




class fcDialog(QDialog, Ui_Form1):
	def __init__(self, parent=None):
		super(fcDialog, self).__init__(parent)
		 #self.figure = plt
		self.setupUi(self)
		fig1 = Figure()
		self.canvas = FigureCanvas(fig1)
		self.histogram.addWidget(self.canvas)
		self.plot = fig1.add_subplot(111)
		self.plot.set_ylim([0, 5000])
		self.plot.set_xlim([0, 256])
		self.canvas.draw()
		self.move(0,0)
		self.Levels=[[0,255],[0,255],[0,255]]

	def setupThreadingUpdates(self, imgthread):
		#set up connections to UI update from imgthread
		self.connect(imgthread, QtCore.SIGNAL("updateFrameNum(int)"), self.updateFrameNum)
		self.connect(imgthread, QtCore.SIGNAL("displayWashouts(PyQt_PyObject, float, float)"), self.displayWashouts)
		self.connect(imgthread, QtCore.SIGNAL("plotHistogram(PyQt_PyObject, PyQt_PyObject, float)"), self.plotHistogram)
		self.connect(imgthread, QtCore.SIGNAL("updateSS(int, int, int)"), self.updateSS)
		self.connect(imgthread, QtCore.SIGNAL("updateGains(int, int)"), self.updateGains)
		self.connect(imgthread, QtCore.SIGNAL("updateStatus(QString)"), self.updateStatus)

#TAB CHANGE CONROLS
	def tabChanged(self,tab):
		if tab == 0:
			if config.captureOn:
				config.captureOn = False
			sendCtrl(CAPTURE_OFF) #to stop capture mode
			if self.prevCheckBox.isChecked():
				sendCtrl(PREVIEW_ON)
		elif tab == 1:
			if not config.captureOn:
				self.autoExpCheckBox.setChecked(False)
				sendCtrl(CAPTURE_ON) #to start capture mode
				#sendCtrl(SPEED+str(self.driveSpeed.value()))
				config.captureOn = True
				config.wait_for_test=True  #switching to capture mode sets the exposure and sends a test pic
		#if tab = 2 (advanced) we leave things at current setting
#SETUP CONTROLS	
	def motorFwd(self):
		sendCtrl(MOTOR_FWD)
	def motorRev(self):
		sendCtrl(MOTOR_REV)
	def motorffd(self):
		sendCtrl(MOTOR_FFD)
	def motorfrev(self):
		sendCtrl(MOTOR_FREV)
        
        
	def motorStop(self):
		sendCtrl(MOTOR_STOP)
	def lightSet(self, isOn):
		sendCtrl(LIGHT_ON if isOn else LIGHT_OFF)
	def previewSet(self, isOn):
		if isOn:
			config.prevOn=isOn
		sendCtrl(PREVIEW_ON if isOn else PREVIEW_OFF)
			#this tells the client to stop sending previews.  Client will send a "t" character
			#to our image thread, which will then set prevOn to False and stop reading from the stream.
	def setAutoExp(self, isOn):
		sendCtrl(AUTOEXP_ON if isOn else AUTOEXP_OFF)
	def setX(self,xval):
		sendCtrl(SETX+str(xval))
		return xval
	def setY(self,yval):
		sendCtrl(SETY+str(yval))
		return yval
	def setZoom(self,zoomval):
		ctrmin=zoomval/2
		ctrmax=1000-ctrmin
		self.xScroll.setRange(ctrmin,ctrmax)
		self.yScroll.setRange(ctrmin,ctrmax)
		sendCtrl(SETZ+str(zoomval))
		return zoomval
	def loadConfig (self):
		startfile = os.path.dirname(str(self.configFile.text()) or config.default_folder)
		myfile = QFileDialog.getOpenFileName(self, "Choose Config File", startfile, "*.ini")
		if myfile:
			self.configFile.setText(myfile)
			self.loadConfigFile(myfile)
	def saveConfig (self):
		startfile = os.path.dirname(str(self.configFile.text()) or config.default_folder)
		myfile = QFileDialog.getSaveFileName(self, "Save New Config File", startfile, "*.ini")
		if myfile:
			myfile = str(myfile)
		if myfile:
			if not myfile.endswith(".ini"):
				myfile += ".ini"
			self.configFile.setText(myfile)
			self.saveConfigFile(myfile)
	def saveCurrentConfig(self):
		if str(self.configFile.text()):
			self.saveConfigFile(str(self.configFile.text()))
		else:
			QMessageBox.warning(self.configFile,"No Config File","No file set: Use 'Save As...'",QMessageBox.Ok)
	def saveConfigFile(self, cnfFile):
		self.config.updateConfigFromUI(self)
		with open(cnfFile, 'wb') as savefile:
			self.config.write(savefile)
	def loadConfigFile(self, cnfFile):
		logging.debug("Reading config file "+cnfFile)
		self.config.read([cnfFile])
		self.config.updateUIfromConfig(self)
		logging.debug("Done reading config file")
# CAPTURE CONTROLS
	def captureStart(self):
		#initialize arrays for smartCapture
		config.frame_number=config.frame_start
		#For Smart Capture Brightness Tracking - Unused Now:  config.brightnessInit(self.prevFrames.value(),self.last4prev.value(),self.initFrames.value(),self.last4init.value())
		#logging.debug(config.prevFrames)
		sendCtrl(START_CAPTURE)
		self.setExposureBtn.setDisabled(True)
		config.wait_for_test=False  #might not be necessary, but if we didn't get an extra frame when stopping it won't set back
	def captureEnd(self):
		sendCtrl(STOP_CAPTURE)
		#if not self.lightCheckbox.isChecked():
		#	sendCtrl(LIGHT_OFF) 
		self.setExposureBtn.setEnabled(True)
		config.wait_for_test=True  #this assumes that we might get an extra frame after sending quit signal
		self.startFrameBox.setValue(config.frame_number)
	def capturePause(self, paused):
		if paused:
			sendCtrl(STOP_CAPTURE)
			self.pauseBox.setEnabled(False)
			sleep(5)  #We switch to test mode, but only after finishing streaming whatever's coming
			self.setExposureBtn.setEnabled(True)
			self.pauseBox.setEnabled(True)
			config.wait_for_test=True  #this assumes that we might get an extra frame after sending quit signal
		else:
			config.wait_for_test=False
			sendCtrl(RESUME_CAPTURE)
	def capFrameAdv(self):
		sendCtrl(CAP_FRAME_ADV)
	def capFrameRev(self):
		sendCtrl(CAP_FRAME_REV)
	def capFrameAdv10(self):
		sendCtrl(CAP_FRAME_ADV+"10")
	def capFrameRev10(self):
		sendCtrl(CAP_FRAME_REV+"10")

	def chooseFolder(self):
		startfolder = os.path.dirname(str(self.configFile.text()) or config.default_folder)
		folder = QFileDialog.getExistingDirectory(self, "Choose Capture Folder", startfolder, QFileDialog.ShowDirsOnly)
		self.setFolder(folder)
	def setFolder(self, folder):
		if folder:
			self.capFolder.setText(folder)
			config.folder=folder
		return folder
	def setBlend(self, bracketing):
		sendCtrl(BRACKETING_SHOTS+str(bracketing))
		config.bracketing = bracketing
		return bracketing
	def setBlendStops(self, stops):
		sendCtrl(BRACKETING_STOPS+str(stops))
		config.blendStops = stops
		return stops
	def setStartFrame(self, startFrame):
		global nextFrame
		config.frame_start = startFrame
	def setEndFrame(self, frame):
		global endFrame
		config.frame_limit = frame
	def setStillPort(self, still):
		sendCtrl(VID_PORT_OFF if still else VID_PORT_ON)
		config.still = still
		return still
	def setExposure(self):
		sendCtrl(FIX_EXPOSURE)
		config.wait_for_test=True #server will be sending a test frame
	def setExposureValue(self, ms):
		sendCtrl(FIX_EXPOSURE+str(ms))
	def setExposureUp(self):
		sendCtrl(SS_SLOWER)
	def setExposureDown(self):
		sendCtrl(SS_FASTER)
	def setDriveSpeed(self, spd):
		sendCtrl(SET_MOTOR_SPEED+str(spd))
	def takeTestPhoto(self):
		config.wait_for_test=True
		sendCtrl(TEST_PHOTO)
	def setCapRes(self,idx):
		sendCtrl(SET_SIZE+str(idx))
		return idx
# COLOR SETTINGS
	def setGainRed(self, gRed):
		sendCtrl(GAIN_RED+str(gRed))
		return gRed
	def resetGainRed(self):
		self.redGainBox.setValue(100)
	def setGainBlue(self, gBlue):
		sendCtrl(GAIN_BLUE+str(gBlue))
		return gBlue
	def resetGainBlue(self):
		self.blueGainBox.setValue(200)
	def setSaturation(self,sat):
		sendCtrl(SATURATION+str(sat))
		return sat
	def resetSaturation(self):
		self.saturationBox.setValue(0)
	def setBright(self, brt):
		sendCtrl(BRIGHTNESS+str(brt))
		return brt
	def setEV(self, ev):
		sendCtrl(EXP_COMP+str(ev))
		return ev
	def resetBright(self):
		self.brightnessBox.setValue(50)
	def setContrast(self, con):
		sendCtrl(CONTRAST+str(con))
		return con
	def resetContrast(self):
		self.contrastBox.setValue(50)
	def colorSet(self):
		box=self.awbBox
		box.setCurrentIndex(box.findText('off'))		
		sendCtrl(FIX_GAINS)
	def setAWBmode(self, awb):
		#self.colorSet.setChecked(False)
		mode = self.awbBox.currentText()
		sendCtrl(AWB_MODE+mode)
		self.setColorsEnabled(mode=='off')
		return awb
	def setColorsEnabled(self, on):
		self.redGain.setEnabled(on)
		self.redGainBox.setEnabled(on)
		self.redResetBtn.setEnabled(on)
		self.blueGain.setEnabled(on)
		self.blueGainBox.setEnabled(on)
		self.blueResetBtn.setEnabled(on)
	def updateGains(self,r,b):
		self.redGain.setValue(r)
		self.redGainBox.setValue(r)
		self.blueGain.setValue(b)
		self.blueGainBox.setValue(b)

	def setAdjLowR(self,val):
		self.Levels[2][0]=val
		self.setNorms(2)
	def setAdjHiR(self,val):
		self.Levels[2][1]=val
		self.setNorms(2)
	def setAdjLowG(self,val):
		self.Levels[1][0]=val
		self.setNorms(1)
	def setAdjHiG(self,val):
		self.Levels[1][1]=val
		self.setNorms(1)
	def setAdjLowB(self,val):
		self.Levels[0][0]=val
		self.setNorms(0)
	def setAdjHiB(self,val):
		self.Levels[0][1]=val
		self.setNorms(0)

	def setNorms(self,color):
		self.lutChannel(color,self.Levels[color][0], self.Levels[color][1])

	def levels2norms(self,low,hi):
		slope=256.0/(hi-low)
		alpha=0-(slope*low)
		beta =256*slope-alpha
		return(alpha, beta)
		
	def lutChannel(self,color,low,hi):
		logging.debug("LOW: %d, HIGH%d"%(low,hi))
		slope=256.0/(hi-low)
		alpha=0-(slope*low)
		beta =256*slope+alpha
		logging.debug(color)
		for i in range(256):
			logging.debug(min(max(i*slope+alpha,0),255))
			config.lut[i][0][color]=min(max(i*slope+alpha,0),255)
# ADVANCED CONTROLS
	def setDrc(self, drc):
		return drc
	def setHFlip(self, isOn):
		sendCtrl(HFLIP_ON if isOn else HFLIP_OFF)
		return isOn
	def setVFlip(self, isOn):
		sendCtrl(VFLIP_ON if isOn else VFLIP_OFF)
		return isOn
	def setBW(self, isOn):
		sendCtrl(BW_ON if isOn else BW_OFF)
		return isOn
	def setSharpness(self,sharp):
		sendCtrl(SHARPNESS+str(sharp))
		return sharp
	def setBlankLimit(self,limit):
		blankLimit=limit
		return limit
	def closeEvent(self, *args, **kwargs):
		super(fcDialog, self).closeEvent(*args, **kwargs)
		sendCtrl(MOTOR_STOP)
		sendCtrl(LIGHT_OFF)
		if config.prevOn:
			sendCtrl(PREVIEW_OFF)
			sleep(1)
		sendCtrl(CLIENT_QUIT)
		logging.debug("Window Close Event")
	def updateSS(self, ss, again, dgain):
		logging.debug("updateSS called")
		self.exposureBox.setValue(ss)
		self.exposureBoxMax.setValue(self.minExp(ss))
		self.exposureBoxMin.setValue(self.maxExp(ss))
		self.gainBoxA.setValue(again)
		self.gainBoxD.setValue(dgain)

	def updateFrameNum(self, i):
		#logging.debug("UpdateFrameNum called")
		self.frameLcd.display(i)
		if i >= config.frame_start+config.frame_limit:
			self.captureEnd()

	def updateStatus(self, status):
		#logging.debug("updateStatus called")
		self.statusBar.setText(status)

	def displayWashouts(self, over, px, avg): #in hindsight, is this really useful?
		logging.debug("DisplayWashouts Called")
		logging.debug(over[1])
		logging.debug(avg)
		logging.debug(px)
		self.pctOverB.setText(adj_for_size(over[0], px))
		self.pctOverG.setText(adj_for_size(over[1], px))
		self.pctOverR.setText(adj_for_size(over[2], px))
		self.pctUnder.setText(adj_for_size(over[3], px))
		self.pctAvg.setText(str(avg))

	def plotHistogram(self, colorhists, grayhist, px):
		global colors
		logging.debug("plotHistogram Called")
		self.plot.cla()
		self.plot.fill(grayhist, color="gray")
		for i,col in enumerate(colors):
			self.plot.plot(colorhists[i],color = col)
		self.plot.set_ylim([0,px/128])
		self.plot.set_xlim([0,256])
		self.canvas.draw()

	def minExp(self, ss):
		if self.bracketing.value()==1:
			return ss
		else:
			expDiff=self.stopsBox.value()/2.0
			return ss/(2**expDiff)

	def maxExp(self, ss):
		if self.bracketing.value()==1:
			return ss
		else:
			expDiff=self.stopsBox.value()/2.0
			return ss*(2**expDiff)
		
