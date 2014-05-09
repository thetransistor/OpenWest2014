# OpenWest 2014 Electronics Project Kit
Created by Devino and theTransistor for OpenWest 2014.

This kit was intended be an interactive form of fun and learning for the 2014 OpenWest conference in Utah. Please enjoy the kit and thank OpenWest for allowing us to do this. 

See us in SB 276 for help soldering your kit, or to answer any questions you may have.

This kit provides a USB interface to 4 RGB LEDs and 2 pushbuttons. It is based on the design of the DigiSpark project from Digistump ( http://digistump.com ). It contains an Arduino bootloader (micronucleus tiny85 from Bluebie https://github.com/Bluebie) and a small program that was created to provide a USB interface to control the LEDs and read from the pushbuttons.


##### What Can I Do With This Thing???
Just about anything. There is not specific purpose. We originally imagined it being used to monitor CPU/Memory utilization or email status, but we're sure you can find things to use it for.

There are 2-3 ways that you can utilize this project
- Interface over USB using Python or C
  - Keep it in it's current state and interface with the USB using our OpenWestKit protocol.
- Reprogram the Micro-controller with the Arduino IDE
  - Download the digispark bootloader / etc from Digistump ( http://digistump.com ) and flash a new Arduino sketch to the board.
- Program the Micro-controller Directly
  - Use AVR Studio (windows) 
  - Use avr-gcc, avr-libc and avrdude (*nix)


##### Using this Kit with Python / C
1. Get the libusb Driver installed. 
  * Available at either http://www.libusb.org/ or http://digistump.com
2. Install the PyUSB library (get Python 2.7 is you don't already)
  * https://github.com/walac/pyusb
3. DigiSpark USB Python Library for libusb 
  * https://github.com/digistump/DigisparkExamplePrograms/tree/master/Python/DigiUSB/source/arduino
4. Plug in your OpenWest Kit and wait for it to fully boot (about 6 seconds)
  * This is because there is a 5 second boot delay programmed into the micronucleus bootloader.
5. Start the OpenWestKitDemo.py that's located in the PythonDemo folder
  * Apologies for the terrible code, lack of time / sleep was a factor here. :S
6. Modify the demo code
  * Send us your improved code so we can post it.


##### Reprogramming the Attiny85 with the Arduino IDE
Follow the directions for the Digispark that are available on http://digistump.com You can find the pinouts for this kit in the Electronics folder. ( The RGB LEDs are on Arduino Digital Pin 2 )

The RGB LEDs are using WS2812b shift registers which allows you to drive all of the RGB LEDs using only a single pin from Microcontroller. There are several Arduino libraries that can easily control these (or you could write your own). for this project, we prefer Adafruits NeoPixel library ( https://github.com/adafruit/Adafruit_NeoPixel ). You can simply load the NeoPixel demo code in the Arduino IDE, change the LED pin to pin 2, compile, and upload.

Also note that when you Compile and Upload new code through the Arduino IDE for this board, you will need to reset the chip. Please look to the Arduino IDE's console for prompts.


##### Enjoy!
We hope that this kit will be enjoyable to everyone. We will be in room SB 276 for the length of the conference. If you have any questions please stop by. We have a few soldering irons set up and ready go.


##### Credits / Thanks
- Ideas / Developement
  - Devino, d3c4f, MindJuju
- Part Sourcing, PCB Design
  - Devino
- Code
  - d3c4f (though he'll probably deny it if cornered)
- Kit Building / Flashing / QC
  - Yukaia, Aarobc, Devino, d3c4f
- Funding & Support
  - OpenWest. <3


##### Contact
- IRC
  - #thetransistor, #dc801 on Freenode
- Email
  - d3c4f@thetransistor.com
