import cv2			#needed for histogram plotting and preview window display
				#need to build and install opencv version 3 to support frame blending
import threading
import struct
import logging
import config
import numpy as np
import io
from time import sleep
from fractions import Fraction
from PyQt4 import QtCore as qtcore
from PyQt4 import QtGui

mask_pct = .8			#this determines what (center) portion of the image is used for histogram calculations. (Avoid using black borders)
blender=cv2.createMergeMertens()   #COMMENT OUT IF NOT USING opencv version 3+ and bracketing

def thefilename(i,suffix=""):
	fname=str(config.folder) + "/img%.5d%s.jpg" % (i,suffix)
	logging.debug(fname)
	return fname
	
def subDims(amt, fraction): #sub dimensions: Pass it a width or height and get the origin and width/height of the center portion
	return(int(amt*(1-fraction)/2),int(amt*(1+fraction)/2))
def getMask(img, fraction):
	mask = np.zeros(img.shape[:2], np.uint8)
	(x,x2,y,y2)=subDims(img.shape[0],fraction)+subDims(img.shape[1],fraction)
	mask[x:x2, y:y2]=255
	return mask

def saveable_img(img):
	return np.array(img,dtype=float)*float(255)

def adjustable_img(img):
	return cv2.convertScaleAbs(img, alpha=255)
	#return np.array(img*float(250),dtype=np.uint8)

def saveable_255_img(img):
	return np.array(img,dtype=float)

def quickBrightness(img):
	#make a thumbnail, convert to grayscale, get avg value
	brt=cv2.mean(cv2.cvtColor(cv2.resize(img, (120,90)),cv2.COLOR_BGR2GRAY))
	brt=int(brt[0]*100)
	logging.debug("Brt="+str(brt))
	return brt

def correctLens(img, w, h):
	distCoeff = np.zeros((4,1),np.float64)
	# TODO: add your coefficients here!
	k1 = config.lensCorrValue # negative to remove barrel distortion
	k2 = 0.0;
	p1 = 0.0;
	p2 = 0.0;
	distCoeff[0,0] = k1;
	distCoeff[1,0] = k2;
	distCoeff[2,0] = p1;
	distCoeff[3,0] = p2;
	# assume unit matrix for camera
	cam = np.eye(3,dtype=np.float32)
	cam[0,2] = w/2.0  # define center x
	cam[1,2] = h/2.0 # define center y
	cam[0,0] = 100.        # define focal length x
	cam[1,1] = 100.        # define focal length y
	# here the undistortion will be computed
	dst = cv2.undistort(img,cam,distCoeff)
	return dst
	
def adjustLevels(img):
	h,w=img.shape[:2]
	#perform lens correction if selected
	if config.lensCorr:
		img=correctLens(img, w, h)
	#perform rotation if selected
	if config.rotation:
		M = cv2.getRotationMatrix2D((w/2,h/2),config.rotationValue,1)
		img = cv2.warpAffine(img,M,(w,h))
	#perform cropping if selected
	if config.cropping:
		img=img[config.cropT:h-config.cropB, config.cropL:w-config.cropR]
	return cv2.LUT(img, config.lut)

class imgThread (qtcore.QThread):#(threading.Thread):
	def __init__(self, connection, app):
		qtcore.QThread.__init__(self, parent=app)
		self.threadID = 1
		self.name = "ImgThread"
		self.conn = connection

	def updateFrameNum(self,i):
		self.emit(qtcore.SIGNAL("updateFrameNum(int)"), i)
	def updateSS(self, ss, again, dgain):
		self.emit(qtcore.SIGNAL("updateSS(int, int, int)"), ss, again, dgain)
	def updateGains(self, r, b):
		self.emit(qtcore.SIGNAL("updateGains(int, int)"), r, b)
	def updateStatus(self,status):
		self.emit(qtcore.SIGNAL("updateStatus(QString)"), status)

	def blendImgList(self,imList,show, fnum):
		logging.debug("Starting blend Thread")
		cvimg=blender.process(imList)
		logging.debug("Done Blending")
		cvimg=adjustLevels(adjustable_img(cvimg))
		#cvimg=adjustable_img(cvimg)
		title=thefilename(fnum)
		if config.wait_for_test:
			title="TEST"
		else:
			cv2.imwrite(thefilename(fnum),cvimg, [int(cv2.IMWRITE_JPEG_QUALITY), 97])
		if config.wait_for_test or show:
			self.showImage(cvimg,title)
		self.plothist(cvimg)#,True)

	def plothist(self, img, fScale=False):   #perhaps this should be called in a separate thread?
		bins=256
		rangetop=1.0 if fScale else 256
		imgsize=img.shape
		mask = getMask(img, mask_pct)
		bwimg=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		bhist = cv2.calcHist([bwimg],[0],mask,[256],[0,rangetop])
		bhist[0]=0
		over = [0,0,0,0]
		over[3]=sum(bhist[:10])
		px = imgsize[0]*imgsize[1]*mask_pct*mask_pct
		ylim=px/128  #arbitrary value to keep y limit consistent and reasonable	
		hists=[]
		for i in range(0,3):
			hist = cv2.calcHist([img],[i],mask,[256],[0,rangetop])
			over[i]=sum(hist[252:])
			hists.append(hist)
		avg=int(cv2.mean(bwimg)[0]*100.0/rangetop)
		#logging.debug("Sending Signal")
		self.emit(qtcore.SIGNAL("plotHistogram(PyQt_PyObject, PyQt_PyObject, float)"), hists, bhist, px)
		self.emit(qtcore.SIGNAL("displayWashouts(PyQt_PyObject, float, float)"), over, px, avg)

	def showImage(self, im, title="Image"):
		im2=cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
		self.emit(qtcore.SIGNAL("displayImg(PyQt_PyObject, QString)"), im2, title)

	def run(self):
		logging.debug("Imgthread running fn")
		image_stream = io.BytesIO()
		imglist = []
		pframe=0 #counter for preview frames, so we only generate histogram 1 in 10 times
		try:
			while not config.exitFlag:
				while config.prevOn or config.captureOn:
					#logging.debug("waiting on img")
					imgflag = self.conn.read(1)
					if imgflag == "q":
						logging.debug(imgflag)
						break
					if imgflag == "f":
						logging.debug(imgflag)
						ss = struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
						again = struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
						dgain = struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
						logging.debug("SS:"+str(ss))
						self.updateSS(ss,again,dgain)
					elif imgflag == "g":
						logging.debug(imgflag)
						r = struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
						b = struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
						logging.debug("Gains "+str(r)+" "+str(b))
						self.updateGains(r,b)
					elif imgflag == "t":
						logging.debug(imgflag)
						config.prevOn = False
						self.showImage(cvimg2, "TEST")
						break
					else:
						if imgflag == "s" or imgflag == "b":
							self.updateFrameNum(config.frame_number)
						image_len = struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
						logging.debug("Image:"+str(image_len))
						if not image_len:
							logging.debug("Quit Signal (0 Length image) received from client")
							break
						#logging.debug(imgflag+str(image_len))
						image_stream.write(self.conn.read(image_len))
						image_stream.seek(0)
						if imgflag == "s": #single image
							cvimg=cv2.imdecode(np.fromstring(image_stream.read(image_len), dtype=np.uint8),1)
							cvimg2=adjustLevels(cvimg)
                            #tmp=image_stream.read(image_len)
							if config.wait_for_test:
								self.showImage(cvimg2,"TEST")
							#else:
							#	process_for_brightness(cvimg)
							self.plothist(cvimg2)
							#logging.debug("Single Shown")
							if not config.wait_for_test:
								filename = thefilename(config.frame_number)
								with open(filename, 'w') as imfile:
									self.showImage(cvimg2, filename)
									cv2.imwrite(filename, cvimg2, [int(cv2.IMWRITE_JPEG_QUALITY), 97])
								self.updateFrameNum(config.frame_number)
								config.frame_number+=1
								#logging.debug("Single Written to "+filename)
						if imgflag == "p": #preview image
							cvimg=cv2.imdecode(np.fromstring(image_stream.read(image_len), dtype=np.uint8),1)
							logging.debug(cvimg.dtype)
							cvimg2=adjustLevels(cvimg)
							self.showImage(cvimg2,"Live Preview")
							pframe+=1
							if pframe>10:
								pframe=0
								self.plothist(cvimg2)							
						if imgflag == "a": #one of several blended images
							#save image data in variable, dont increment or update display
							logging.debug('start a')
							imglist.append(cv2.imdecode(np.fromstring(image_stream.read(image_len), dtype=np.uint8),1))
						if imgflag == "b": #the last of several blended images
							#logging.debug('start read final')
							imglist.append(cv2.imdecode(np.fromstring(image_stream.read(image_len), dtype=np.uint8),1))
							self.updateStatus(str(config.frame_number)+' '+' '.join(map(str,map(quickBrightness,imglist))))
							thd=threading.Thread(target=self.blendImgList, args=(imglist[:],True,config.frame_number)) #colon in brackets makes new copy of list
							thd.start() #tried this using multiprocessing, but it hung when processing merge_mertens
							imglist=[]
							if not config.wait_for_test:
								config.frame_number+=1
					image_stream.seek(0)
					image_stream.truncate()
				#logging.debug("Waiting for prevOn...")
				sleep(1)
		finally:
			logging.debug("Thread closing %.1d"%config.exitFlag)
			cv2.destroyAllWindows()	
			self.conn.close()

