#/usr/bin/python

# Dependencies:
#  PyUSB 1.0 (w/libusb 1.0.3) 
#    https://github.com/walac/pyusb
#  DigiSpark USB Python Library for libusb 
#    https://github.com/digistump/DigisparkExamplePrograms/tree/master/Python/DigiUSB/source/arduino


import time

from arduino.usbdevice import ArduinoUsbDevice

# Attempts to connect to a compatible device
def connectDevice():
   print "Connecting Device"
   
   deviceBound = 0
   while (deviceBound == 0):
      deviceBound = 1
      try:
         openWestKit = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
      except:
         #sys.exit("No Compatible USB Device Found")
         print "Waiting for compatible device to become available"
         deviceBound = 0
         time.sleep(1)


def clearBuffer():
   for temp in range(0,4):
      sendByteToDevice(0)

# Sends a byte to the device
def sendByteToDevice(data):
   try:
      openWestKit.write(data)
   except:
      connectDevice() # Try to rebind the device
      print "couldn't send byte. oh noes"
      return 0
   return 1


# Sets the master brightness on the device (0-255)
def setBrightness(bright):
   print "Setting master brightness to: ",bright
   done = 0
   while(done == 0):
      if(sendByteToDevice(42)):
         if(sendByteToDevice(255)):
            if(sendByteToDevice(bright)):
               done = 1


# Sets a Pixel to RGB value (0-3, 0-255, 0-255, 0-255)
def setPixel(pixelNum, redByte, greenByte, blueByte):
   print "Setting pixel [",pixelNum,"] to values: ",redByte,greenByte,blueByte
   done = 0
   while(done == 0):
      if(sendByteToDevice(42)):
         if(sendByteToDevice(pixelNum)):
            if(sendByteToDevice(redByte)):
               if(sendByteToDevice(greenByte)):
                  if(sendByteToDevice(blueByte)):
                     done = 1


# Initializes the device
def initializeDevice():
   setBrightness(255)
   time.sleep( 1 )
   setBrightness(64)


# Main
if __name__ == "__main__":
   try:
      openWestKit = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
   except:
      #sys.exit("No Compatible USB Device Found")
      deviceBound = 0
      time.sleep(1)
      connectDevice()

   print "Starting..."

   initializeDevice()
   
   while (1):
      for pixelNum in range(0,4):
         setPixel(pixelNum,255,0,0)
         time.sleep( .01 )
         setPixel(pixelNum,0,255,0)
         time.sleep( .01 )
         setPixel(pixelNum,0,0,255)
         time.sleep( .01 )
         setPixel(pixelNum,0,0,0)
         time.sleep( .01 )

