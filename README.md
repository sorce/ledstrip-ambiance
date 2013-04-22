ledstrip-ambiance
=================

ambilight clone using python, an arduino and an lpd8806 based ledstrip.

Modules used:

https://github.com/adafruit/LPD8806
  - library for controlling the chips on the ledstrip

https://github.com/arduino/Arduino/tree/master/libraries/SPI

https://github.com/ludios/Desktopmagic
  - module for grabbing screenshots in PIL format from win32 systems, made by ludios

NOTES:
* line 59 of HardwareSerial.cpp for arduino has been edited to make the serial buffer 98 bytes instead of 64
* Highly specific to my own setup right now; Hardcoded values like sector_length important to functioning
