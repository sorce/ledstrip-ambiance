CXX=avr-gcc
INCLUDE=-I C:/Users/rubix/include/arduino
LIBS=-L C:/Users/rubix/lib -lm -larduino
MCU=-mmcu=atmega328p
CPU_SPEED=-DF_CPU=16000000UL
CFLAGS=$(MCU) $(CPU_SPEED) -Os -w -Wl,--gc-sections -ffunction-sections -fdata-sections
PORT=COM12

default: build upload

build: main.hex

main.hex: main.elf
	avr-objcopy -O ihex $< $@

OBJECTS= LPD8806.cpp SPI.cpp HardwareSerial.cpp
main.elf: main.cpp $(OBJECTS)
	$(CXX) $(CFLAGS) $(INCLUDE) $^ -o $@ $(LIBS)

upload:
	avrdude -V -F -p m328p -c arduino -b 115200 -Uflash:w:main.hex -P$(PORT)

clean:
	@echo -n Cleaning ...
	$(shell rm main.elf 2> /dev/null)
	$(shell rm main.hex 2> /dev/null)
	$(shell rm *.o 2> /dev/null)
	@echo " done"

%.o: %.cpp
	$(CXX) $< $(CFLAGS) $(INCLUDE) -c -o $@
