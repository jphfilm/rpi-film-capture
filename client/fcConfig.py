import ConfigParser
from time import sleep

#A module to save settings to (and restore them from) a config file.
class fcConfigParser(ConfigParser.SafeConfigParser):
	def updateUIfromConfig(self,ui):
		if not self.has_section('Camera'):
			self.add_section('Camera')
		if not self.has_section('Capture'):
			self.add_section('Capture')
		if not self.has_section('Smartcap'):
			self.add_section('Smartcap')
		sec='Camera'
		#Zoom
		ui.zoomDial.setValue(self.getint(sec,'zoom'))#(ui.setZoom(self.getint(sec,'zoom')))
		ui.xScroll.setValue(self.getint(sec,'x'))#(ui.setX(self.getint(sec,'x')))
		ui.yScroll.setValue(self.getint(sec,'y'))#(ui.setY(self.getint(sec,'y')))

		#Color/Brightness
		ui.awbBox.setCurrentIndex(ui.awbBox.findText(self.get(sec,'awb'))) #(ui.setAWBmode(self.get(sec,'awb')))) #this must be done before setting gains
		sleep(.1)
		ui.redGainBox.setValue(ui.setGainRed(self.getint(sec,'redgain')))
		sleep(.2)
		ui.blueGainBox.setValue(ui.setGainBlue(self.getint(sec,'bluegain')))
		ui.saturationBox.setValue(ui.setSaturation(self.getint(sec,'saturation')))
		ui.brightnessBox.setValue(ui.setBright(self.getint(sec,'brightness')))
		ui.EV.setValue(ui.setEV(self.getint(sec,'ev')))
		ui.contrastBox.setValue(ui.setContrast(self.getint(sec,'contrast')))
		ui.levelLowR.setValue(self.getint(sec,'lowr'))
		ui.levelLowG.setValue(self.getint(sec,'lowg'))
		ui.levelLowB.setValue(self.getint(sec,'lowb'))
		ui.levelHiR.setValue(self.getint(sec,'hir'))
		ui.levelHiG.setValue(self.getint(sec,'hig'))
		ui.levelHiB.setValue(self.getint(sec,'hib'))
		

		#Advanced
		ui.stillCap.setChecked(ui.setStillPort(self.getboolean(sec,'usestillport')))
		ui.vflip.setChecked(ui.setVFlip(self.getboolean(sec,'vflip')))
		ui.hflip.setChecked(ui.setHFlip(self.getboolean(sec,'hflip')))
		ui.bw.setChecked(ui.setBW(self.getboolean(sec,'bw')))
		ui.sharpnessBox.setValue(ui.setSharpness(self.getint(sec,'sharpness')))
		ui.drcBox.setCurrentIndex(ui.drcBox.findText(ui.setDrc(self.get(sec,'drc'))))

		sec='Capture'
		ui.capFolder.setText(ui.setFolder(self.get(sec,'capfolder')))	
			#Bracketing/blending settings
		ui.stopsBox.setValue(ui.setBlendStops(self.getfloat(sec,'blendstops')))
		ui.bracketing.setValue(self.getint(sec,'bracketing'))
			#Auto speed settings
		ui.resolution.setCurrentIndex(ui.setCapRes(self.getint(sec,'resolution')))
		
#		sec='Smartcap'
#		ui.blankFrameLimit.setValue(ui.setBlankLimit(self.getint(sec,'blanklimit')))
#		ui.deltaBrt.setValue(self.getint(sec,'deltabrt'))
#		ui.deltaSS.setValue(self.getint(sec,'deltass'))
#		ui.last4init.setValue(self.getint(sec,'last4init'))
#		ui.initFrames.setValue(self.getint(sec,'initframes'))
#		ui.last4prev.setValue(self.getint(sec,'last4prev'))
#		ui.prevFrames.setValue(self.getint(sec,'prevframes'))
#		ui.initPct.setValue(self.getint(sec,'initpct'))
#		ui.initAction.setCurrentIndex(self.getint(sec,'initaction'))
#		ui.prevPct.setValue(self.getint(sec,'prevpct'))
#		ui.prevAction.setCurrentIndex(self.getint(sec,'prevaction'))

	def updateConfigFromUI(self,ui):
		if not self.has_section('Camera'):
			self.add_section('Camera')
		if not self.has_section('Capture'):
			self.add_section('Capture')
		if not self.has_section('Smartcap'):
			self.add_section('Smartcap')
		sec='Camera'
		self.set(sec,'redgain',		str(ui.redGainBox.value()))
		self.set(sec,'bluegain',	str(ui.blueGainBox.value()))
		self.set(sec,'saturation',	str(ui.saturationBox.value()))
		self.set(sec,'brightness',	str(ui.brightnessBox.value()))
		self.set(sec,'contrast',	str(ui.contrastBox.value()))
		self.set(sec,'x',			str(ui.xScroll.value()))
		self.set(sec,'y',			str(ui.yScroll.value()))
		self.set(sec,'zoom',		str(ui.zoomDial.value()))
		self.set(sec,'vflip',		str(ui.vflip.isChecked()))
		self.set(sec,'hflip',		str(ui.hflip.isChecked()))
		self.set(sec,'bw',			str(ui.bw.isChecked()))
		self.set(sec,'sharpness',	str(ui.sharpnessBox.value()))
		self.set(sec,'drc',			str(ui.drcBox.currentText()))
		self.set(sec,'awb',			str(ui.awbBox.currentText()))
		self.set(sec,'ev',			str(ui.EV.value()))
		self.set(sec,'usestillport',str(ui.stillCap.isChecked()))

		self.set(sec,'lowr',			str(ui.levelLowR.value()))
		self.set(sec,'lowg',			str(ui.levelLowG.value()))
		self.set(sec,'lowb',			str(ui.levelLowB.value()))
		self.set(sec,'hir',			str(ui.levelHiR.value()))
		self.set(sec,'hig',			str(ui.levelHiG.value()))
		self.set(sec,'hib',			str(ui.levelHiB.value()))
		
		sec='Capture'
		self.set(sec,'capfolder',	str(ui.capFolder.text()))
		self.set(sec,'blendstops',	str(ui.stopsBox.value()))
		self.set(sec,'bracketing',	str(ui.bracketing.value()))
		self.set(sec,'resolution',	str(ui.resolution.currentIndex()))

#		sec='Smartcap'
#		self.set(sec,'blanklimit',	str(ui.blankFrameLimit.value()))
#		self.set(sec,'deltabrt',	str(ui.deltaBrt.value()))
#		self.set(sec,'deltass',		str(ui.deltaSS.value()))
#		self.set(sec,'last4init',	str(ui.last4init.value()))
#		self.set(sec,'initframes',	str(ui.initFrames.value()))
#		self.set(sec,'last4prev',	str(ui.last4prev.value()))
#		self.set(sec,'prevframes',	str(ui.prevFrames.value()))
#		self.set(sec,'initpct',		str(ui.initPct.value()))
#		self.set(sec,'prevpct',		str(ui.prevPct.value()))
#		self.set(sec,'initaction',	str(ui.initAction.currentIndex()))
#		self.set(sec,'prevaction',	str(ui.prevAction.currentIndex()))
		
		
		
		
		
		

