#!/usr/bin/env python

from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

import sys
import time
import serial
from PIL import Image, ImageGrab

numLeds = 32
screens = getDisplayRects()
#Note that screens[0] is the primary screen, regardless of orientation(left/right)

arduino = serial.Serial('COM12', 9600, timeout=1)
serial.Serial.flush(arduino)

def main():
	#1600x1200, 1920x1080 -- resolutions used by me (so comments can make sense)
	while True:
		img_sectors = getSectors(tophalf=True)
		for sector in img_sectors:
			
			r, g, b = average_image_color(sector)
			
			arduino.write(chr(r))
			arduino.write(chr(g))
			arduino.write(chr(b))
			
			
		serial.Serial.flush(arduino) #flushing 3 * 32 = 96 bytes
	

def getSectors(tophalf=False):
	sector = [] # list of PIL images of sectors of the screen (len should be equal to numLeds)
	(mainx1, mainy1, mainx2, mainy2) = screens[0]
	(secx1, secy1, secx2, secy2) = screens[1]
	
	#need to get the total screen_x length
	sector_length = ( abs(mainx2) + abs(secx1) ) / (numLeds - 1) #Note: 3520/31=113 and this is not completely correct -- particulary for the last picture
	#may want to experiment with better sector_length values
	#sector_length = 120
	div = 1
	if tophalf:
		div = 2 # used in last parameter of getarea when appended to sector below
	
	halfnumleds = numLeds / 2
	
	for x in range(numLeds):
		# Note that case 14 produces a bad image -- and that the last part of the desktop(rightmost) is lost -- due to inprecision of sector_length
		# We could handle this case specially... however I think there's a better solution I've yet to find. The effect of this error doesn't bother me.
		if x * sector_length < abs(secx1): #left screen, screen[1]; a second monitor on the left will have a negative value
			sector.append(getRectAsImage( (secx1 + (x * sector_length), secy1, secx1 + (x * sector_length) + sector_length, secy2 / div)) )
		else: #right (main) screen, screen[0]
			#note that we can't use same maths as above, seeing as the right screen will start at screen coord 0,0 but x is at numLeds / 2
			sector.append(getRectAsImage( (0 + ((x - halfnumLeds) * sector_length), 0, 0 + ((x - halfnumLeds) * sector_length) + sector_length,  mainy2 / div)) )
		
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