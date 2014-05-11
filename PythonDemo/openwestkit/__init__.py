import time

from arduino.usbdevice import ArduinoUsbDevice


# Generic class for interacting with the OpenWest 2014 Electronics Kit
#
# Provides methods to simplify settings LED's and reading button presses.
class OpenWestKit:

    def __init__(self, debug=False):
        self.DEBUG = debug
        self.connect()

        self.brightness(255)
        time.sleep(1)
        self.brightness(64)
        self.clear()

    def connect(self):
        if self.DEBUG:
            print "Connecting Device"

        deviceBound = False
        while(not deviceBound):
            try:
                self.device = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
                deviceBound = True
            except Exception as e:
                print "Problem connecting:", e
                time.sleep(1)
                print 'retrying...'

    # Sends a byte to the device
    def sendByteToDevice(self, data):
        try:
            self.device.write(data)
        except Exception as e:
            print "Unable to write to device:", e
            self.connect()  # Try to rebind the device
            return 0
        return 1

    # Read all data off the bus. Multiple codes may be waiting so we keep
    # reading until there is no more data. We then return it all in an array.
    # Codes:
    # z - Acknowledgement of LED set command
    # a - Button 1 pressed
    # b - Button 2 pressed
    def readData(self):
        result = []
        while(True):  # keep reading while we have data
            try:
                result.append(str(unichr(self.device.read())))
            except:
                break
        return result

    # Sets the master brightness on the device (0-255)
    def brightness(self, bright):
        if self.DEBUG:
            print "Setting master brightness to: ", bright
        while(True):
            if(self.sendByteToDevice(42)):  # LED control code
                if(self.sendByteToDevice(255)):  # Brightness control code
                    if(self.sendByteToDevice(bright)):  # brightness amount
                        break

    # Sets a Pixel to RGB value (0-3, 0-255, 0-255, 0-255)
    def setPixel(self, pixelNum, redByte, greenByte, blueByte):
        if self.DEBUG:
            print "Setting pixel [ %s ] to values: %s, %s, %s" % (pixelNum, redByte, greenByte, blueByte)
        while(True):
            if(self.sendByteToDevice(42)):  # LED control code
                if(self.sendByteToDevice(pixelNum)):  # LED position control code
                    if(self.sendByteToDevice(redByte)):
                        if(self.sendByteToDevice(greenByte)):
                            if(self.sendByteToDevice(blueByte)):
                                break

    # Reset board to starting state with Red, Green, Blue, White LED
    def reset(self):
        self.brightness(10)
        self.setPixel(0, 255, 0, 0)
        self.setPixel(1, 0, 255, 0)
        self.setPixel(2, 0, 0, 255)
        self.setPixel(3, 255, 255, 255)

    # Helper method to turn all LEDs off
    def clear(self):
        self.setPixel(0, 0, 0, 0)
        self.setPixel(1, 0, 0, 0)
        self.setPixel(2, 0, 0, 0)
        self.setPixel(3, 0, 0, 0)
