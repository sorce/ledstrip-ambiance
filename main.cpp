#include "LPD8806.h"
#include "SPI.h"
#include "WProgram.h"

int CheckForColors();

int nLEDs = 32;
int dataPin = 2;
int clockPin = 3;

char rgb[32][3]; // nLEDs amount of R/G/B values [in decimal]
int ret = 0;

LPD8806 strip = LPD8806(nLEDs, dataPin, clockPin);
//LPD8806 strip = LPD8806(nLEDs); // use hardware SPI - pins MUST be: clock = 11, data = 13

//****************************************************************************

void setup() 
{
	memset(rgb, 0, sizeof rgb);
	
	Serial.begin(9600);
	
	strip.begin();
	strip.show();
}

void loop() 
{
	ret = CheckForColors();
	if (ret == 0) {
		//successfully read one strips worth of colors
		for (int x = 0; x < strip.numPixels(); x++) {
			strip.setPixelColor(x, strip.Color(rgb[x][0], rgb[x][1], rgb[x][2]));
			//strip.show();
		}
		strip.show();
	}
}

int CheckForColors() //Note: serial buffer only holds 64 bytes of data (defined on line 60 HardwareSerial.cpp)
{
	int o, i;
	while (Serial.available()) {
		if (Serial.available() >= 3 * 32) { // 3 * 32  = 96 bytes to be read
			//serial buffer holds only 64 bytes of data as defined on line 59 in HardwareSerial.cpp
			//I've edited this to hold 98 bytes instead of actually fixing the below code
			for (o = 0; o < nLEDs; o++) {
				for (i = 0; i < 3; i++) {
					rgb[o][i] = Serial.read();
				}
				rgb[o][0] = map(rgb[o][0], 0, 255, 0, 127);
				rgb[o][1] = map(rgb[o][1], 0, 255, 0, 127);
				rgb[o][2] = map(rgb[o][2], 0, 255, 0, 127);
			}
			
			return 0;
		}
	}
	return 1;
}

int main() 
{
	init();
	setup();
	while(1)
		loop();
}
