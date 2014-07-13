/*
	FILENAME:		OpenWest2014_kit.ino
	CREATION DATE:	2014.05.06
	AUTHOR(S):		(aarobo, d3c4f)
	DESCRIPTION:
		Basic quick-n-dirty code for "Learn to Solder OpenWest Electronics Kit". Allows for control of the board over USB serial using the DigiUSB and libusb libraries. For basic usage, you will not need to reflash the board with additional code; check out the python script for interaction with your computer.
	LIBRARY INFORMATION: 
		- DigiUSB: For sending serial data over USB. Available with the DigiSpark Arduino Setup. See: http://digistump.com/wiki/digispark/tutorials/connecting direct code is available on: https://github.com/digistump
		- NeoPixel: This is the library we are using to control the RGB LEDs with the WS2812b shift registers. You can get a copy of the library at: https://github.com/adafruit/Adafruit_NeoPixel
	ADDITIONAL NOTE(S):
		- The "Learn to Solder OpenWest Electronics Kit" is built around the Atmel Attiny85 MicroProcessor.
		- We are using the digistump arduino and usb libraries. For more information, please visit http://digistump.com
		- The Microcontrollers in this kit all come preloaded with this software. 
		- If you get new / better code going. LET me know ASAP and we'll get it updated for everyone. :)
		- Han shot first.
	CONTACT:
		email: d3c4f@thetransistor.com
		irc: #thetransistor on Freenode
*/

#include <DigiUSB.h>
#include <Adafruit_NeoPixel.h>

#define PIXELPIN 2	// The Arduino Digital Pin Address of the Data Pin. Physical pin number is 7 on the Attiny85 mCU
#define BUTTON1 1	// Arduino 'pin' for pushbutton 1
#define BUTTON2 0	// Arduino 'pin' for pushbutton 2
#define DTIME 80	// Number of Milliseconds to debounce pushbuttons

// Globals. Yes this could be in a library, and probably should!
int lastByte;
int commandBuffer[8];
int commandBufferPos = -1;
long lastButton1; // button1 debounce counter
long lastButton2; // button2 debounce counter
long lastButton1up; // button1 release debounce counter 
long lastButton2up; // button2 release debounce counter

// Setup the "NeoPixel strip".
Adafruit_NeoPixel strip = Adafruit_NeoPixel(4, PIXELPIN, NEO_GRB + NEO_KHZ800);


// FUNCTION: setup()
// PURPOSE: Setup Code. Arduino is weird this way.
void setup() {
	DigiUSB.begin();			// Initialize the USB Serial
	
	pinMode(BUTTON1, INPUT);		// Set to input
	pinMode(BUTTON2, INPUT);		// Set to input
	digitalWrite(BUTTON1, HIGH);	// Set internal pull-up resistor
	digitalWrite(BUTTON2, HIGH);	// Set internal pull-up resistor

	strip.begin();				// Initialize a strip of LEDs
	strip.setBrightness(32);	// Set initial brightness (0-255)
	strip.show();				// Initialize all pixels to 'off' by updating with initial values.
}


// FUNCTION: loop()
// PURPOSE: In Arduino, main() is replaced with an infinite loop
void loop() {
	DigiUSB.refresh();
	startupBlink();		// Blink a couple times to let you know it's online
	
	while(true){
		DigiUSB.refresh();
		process_buffer();	// Process the USB buffer
		
		// Check Pushbutton 1

		if(process_pushbutton(digitalRead(BUTTON1), lastButton1)){
			DigiUSB.write('a');
		}
		
		// Check Pushbutton 2
		if(process_pushbutton(digitalRead(BUTTON2), lastButton2)){
			DigiUSB.write('b');
		}

		// Check Pushbutton 1 up
		if(process_pushbutton(!digitalRead(BUTTON1), lastButton1up)){
			DigiUSB.write('A');
		}
		
		// Check Pushbutton 2 up
		if(process_pushbutton(!digitalRead(BUTTON2), lastButton2up)){
			DigiUSB.write('B');
		}


	}
}


// FUNCTION: process_buffer()
// PURPOSE: Processes the USB buffer.
// DESCRIPTION: Looks for a start byte of value of 42. Once we receive the start byte, we will read in a full command
// PROTOCOL: [Start Byte, 00101010][Command Byte][Value Byte(s)]
//		Command Byte DEC Value of 0-3 is Set LED # RBG. Expects 3 Value Bytes
//		Command Byte DEC Value of 255 is Set Master Brightness. Expects 1 Value Byte
void process_buffer(){
	// Check if there is data available for us to read in
	if (DigiUSB.available()) {
		lastByte = (int)DigiUSB.read(); // Read a byte of the information in!
		
		// Determine Stage
		if (commandBufferPos == -1){
			// Waiting for a Start Byte
			if(lastByte == 42){
				// Found a start byte!
				commandBufferPos = 0;
			}
			
		} else if (commandBufferPos == 0){
			// Looking for a valid Command Byte
			switch (lastByte) {
				case 0: // LED 1
				case 1: // LED 2
				case 2: // LED 3
				case 3: // LED 4
				case 255: // Set master brightness
					commandBuffer[0] = lastByte;
					commandBufferPos = 1;
					break;
					
				default: // Unknown command.
					commandBufferPos = -1;
			}
			
		} else {
			// Processing values
			switch (commandBuffer[0]) {
				case 0: // LED 1
				case 1: // LED 2
				case 2: // LED 3
				case 3: // LED 4
					// After we get RGB values, process it and reset.
					commandBuffer[commandBufferPos] = lastByte;
					if(commandBufferPos == 3) {
						strip.setPixelColor(commandBuffer[0], commandBuffer[1], commandBuffer[2], commandBuffer[3]);
						strip.show();
						DigiUSB.write('z');
						commandBufferPos = -1; // Next command, pl0x
						break;
					}
					commandBufferPos++;
					break;
					
				case 255: // Set master brightness
					strip.setBrightness(lastByte);
					strip.show();
					DigiUSB.write('z');
					commandBufferPos = -1; // Next command, pl0x
					break;
					
				default: // Unknown command. Reset
					DigiUSB.write('u');
					commandBufferPos = -1;
			}
		}
	}
}

// FUNCTION: process_pushbutton(active, timestamp)
// PURPOSE: Debounce pushbutton
bool process_pushbutton(int state, long &timestamp){
	if(!state){
		if(timestamp > 0){
			if(millis() > timestamp + DTIME) {
				timestamp = 0; // Stop reporting button pressed, until button is reset
				return true;
			} else {
				return false;
			}
		} else {
			if(timestamp == -1) timestamp = millis(); // Wait for reset, before counting again...
			return false;
		}
	} else {
		timestamp = -1; // Reset / Stage for next press
		return false;
	}
}

// FUNCTION: startupBlink()
// PURPOSE: Blinks the leds to let you know it's ready. :)
void startupBlink(){
	strip.setPixelColor(0, 255, 255, 255);
	strip.show();
	delay(100);

	strip.setPixelColor(0, 0, 0, 0);
	strip.setPixelColor(1, 255, 255, 255);
	strip.show();
	delay(100);
	
	strip.setPixelColor(1, 0, 0, 0);
	strip.setPixelColor(2, 255, 255, 255);
	strip.show();
	delay(100);
	
	strip.setPixelColor(2, 0, 0, 0);
	strip.setPixelColor(3, 255, 255, 255);
	strip.show();
	delay(100);
	
	strip.setPixelColor(3, 0, 0, 0);
	strip.show();
	delay(100);
	
	strip.setPixelColor(0, 100, 100, 100); strip.setPixelColor(1, 100, 100, 100);
	strip.setPixelColor(2, 100, 100, 100); strip.setPixelColor(3, 100, 100, 100);
	strip.show();
	delay(150);

	strip.setPixelColor(0, 0, 0, 0); strip.setPixelColor(1, 0, 0, 0);
	strip.setPixelColor(2, 0, 0, 0); strip.setPixelColor(3, 0, 0, 0);
	strip.show();
	delay(150);

	strip.setPixelColor(0, 100, 0, 0); strip.setPixelColor(1, 0, 100, 0);
	strip.setPixelColor(2, 0, 0, 100); strip.setPixelColor(3, 100, 100, 100);
	strip.show();
}


