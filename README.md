ledstrip-ambiance
=================

ambilight clone using python2.7, an arduino uno and an lpd8806 based digital ledstrip (http://www.adafruit.com/products/306).

to see it in action: https://www.youtube.com/watch?v=I3s4oOG_eAM

Libraries / Modules used:
=========================

https://github.com/ludios/Desktopmagic
  - module for grabbing screenshots in PIL format from win32 systems, made by ludios

https://github.com/adafruit/LPD8806
  - library for controlling the chips on the ledstrip

https://github.com/arduino/Arduino/tree/master/libraries/SPI

http://www.pythonware.com/products/pil/


NOTES:
======
* line 59 of HardwareSerial.cpp for arduino has been edited to make the serial buffer 98 bytes instead of 64
* Highly specific to my own setup right now; Hardcoded values like sector_length important to functioning
