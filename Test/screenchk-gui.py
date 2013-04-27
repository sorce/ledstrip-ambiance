#!/usr/bin/env/python

from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

import sys, os
from PIL import Image

from PyQt4 import QtGui


numLeds = 32

screens = getDisplayRects()

class ScreenColors(QtGui.QWidget):
	def __init__(self):
		super(ScreenColors, self).__init__()
		
		self.forms = []
		
		self.InitUI()
	
	def InitUI(self):
		#create forms
		self.squareSize = 25
		self.setGeometry(50, 50, 512, 356)
		
		for x in range(numLeds):
			self.forms.append(QtGui.QFrame(self))
			self.forms[x].setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(0,155,155).name())
			if x < numLeds / 2:
				self.forms[x].setGeometry(x * (self.squareSize * 1.2), self.height() / 4, self.squareSize, self.squareSize)
			else:
				self.forms[x].setGeometry((0 + (x - (numLeds / 2))) * (self.squareSize * 1.2), self.height() / 2, self.squareSize, self.squareSize)
				
		
		self.btn = QtGui.QPushButton('update', self)
		self.btn.move(10, 25)
		self.btn.clicked.connect(self.onUpdate)
		
		self.setWindowTitle('color tester')
		self.show()
		#self.UpdateForms()
		
		
		#for ims in img_sectors:
		#	r,g,b = average_image_color(ims)
		#	color = QtGui.QColor(r, g, b)
			
	
	def onUpdate(self):
		self.UpdateForms()
	
	def UpdateForms(self):
		img_sectors = getSectors(tophalf=True)
		for x in range(numLeds):
			r, g, b = average_image_color(img_sectors[x])
			color = QtGui.QColor(r, g, b)
			self.forms[x].setStyleSheet("QWidget { background-color: %s }" % color.name())
			
	
	def printAverages(self, img_secs):
		for imsec in img_secs:
			print average_image_color(imsec)

def main():
	# 1600x1200, 1920x1080
	app = QtGui.QApplication(sys.argv)
	cc = ScreenColors()
	sys.exit(app.exec_())
	

def getSectors(tophalf=False):
	sector = [] # list of PIL images of sectors of the screen (len should be equal to numLeds)
	
	(mainx1, mainy1, mainx2, mainy2) = screens[0]
	(secx1, secy1, secx2, secy2) = screens[1]
	
	#sector_length = ( abs(mainx2) + abs(secx1) ) / numLeds #NOTE: 3520/32=110 and this is NOT CORRECT
	sector_length = 120
	
	div = 1
	if tophalf:
		div = 2 # used in last parameter of getarea when appended to sector below
	
	halfnumLeds = numLeds / 2
	
	for x in range(numLeds):
		"""if x == 15: #15 is a special case because it's the 16th (halfway) led, and needs to be handled specially
			sector.append(getRectAsImage( () ))"""
		#if x  < halfnumLeds: # left screen, screen_coords[1]
		if x * sector_length < 1600:
			#						50, -344, 160, 856
			#					      -1600 + (15 * 110), -344, -1600 + (15 * 110) + 110, 856 / 1
			sector.append(getRectAsImage( (secx1 + (x * sector_length), secy1, secx1 + (x * sector_length) + sector_length, secy2 / div)) )
		else: #right screen, screen_coords[0]
			#note that we can't use same maths as above, seeing as the right screen will start at screen coord 0,0 but x is at numLeds / 2
			sector.append(getRectAsImage( (0 + ((x - halfnumLeds) * sector_length), 0, 0 + ((x - halfnumLeds) * sector_length) + sector_length,  mainy2 / div)) )
		#							0 + ((16 - 16) * 0, 0, 0 + ((16 - 16) * 0) + 110,  1080
		#							0, 0, 110, 1080
		#							0 + ((32-16)*110), 0, 0+((32-16)*110)+110,1080
		#							1760, 0, 1870, 1080
	return sector

def average_image_color(i):
	h = i.histogram()

	# split into red, green, blue
	r = h[0:256]
	g = h[256:256*2]
	b = h[256*2: 256*3]

	# perform the weighted average of each channel:
	# the *index* is the channel value, and the *value* is its weight
	return (
		sum( i*w for i, w in enumerate(r) ) / sum(r),
		sum( i*w for i, w in enumerate(g) ) / sum(g),
		sum( i*w for i, w in enumerate(b) ) / sum(b)
	)

if __name__ == '__main__':
	main()