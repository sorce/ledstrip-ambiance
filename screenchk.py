#!/usr/bin/env python

from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

import sys
import time
#import serialArduino as serial #serialArduino edits serialWin32.py to disable DTR control
import serial

from PIL import Image, ImageGrab

numLeds = 32

screens = getDisplayRects()
screen_coords = [] # list of rects ((left, top, right, bottom)) defining each screen
screen_coords.append(rect for rect in screens) 
#NOTE that screen_coords[0] is the primary screen, regardless of orientation(left/right)

#arduino = serial.Serial('COM12', 9600, timeout=0)
arduino = serial.Serial('COM12', 9600, timeout=1)
serial.Serial.flush(arduino)

def main():
	#1600x1200, 1920x1080
	
	while True:
	#for i in range(1):
		img_sectors = getSectors(tophalf=True)
		#img_sectors = getSectors(tophalf=False)
		#img_sectors.reverse()
		for sector in img_sectors:
			
			r, g, b = average_image_color(sector)
			
			arduino.write(chr(r))
			arduino.write(chr(g))
			arduino.write(chr(b))
			
			
		serial.Serial.flush(arduino) #flushing 3 * 32 = 96 bytes
	

def getSectors(tophalf=False):
	sector = [] # list of PIL images of sectors of the screen (len should be equal to numLeds)
	#sector_length = screen_x / numLeds #3520 / 32 = 110 NOTE that this number is NOT ACCURATE!!!
	#need to get the total screen_x length
	#sector_length = ( abs(screen_coords[0][2]) + abs(screen_coords[1][0]) ) / numLeds
	(mainx1, mainy1, mainx2, mainy2) = screens[0]
	(secx1, secy1, secx2, secy2) = screens[1]
	
	#sector_length = ( abs(mainx2) + abs(secx1) ) / numLeds # 3520 / 32 = 110
	sector_length = 120
	
	div = 1
	if tophalf:
		div = 2 # used in last parameter of getarea when appended to sector below
	
	
	halfnumleds = numLeds / 2
	
	for x in range(numLeds):
		#if x  < halfnumleds: # left screen, screen_coords[1]
		if x * sector_length < 1600: # left screen, screen_coords[0]
			sector.append(getRectAsImage( (secx1 + (x * sector_length), secy1, secx1 + (x * sector_length) + sector_length, secy2 / div)) )
		else: #right screen, screen_coords[0]
			#note that we can't use same maths as above, seeing as the right screen will start at screen coord 0,0 but x is at numLeds / 2
			sector.append(getRectAsImage( (0 + ((x - halfnumleds) * sector_length), 0, 0 + ((x - halfnumleds) * sector_length) + sector_length,  mainy2 / div)) )
		
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