# Shows the LEDs with a Red, Green, Blue, White color and the buttons raise and
# lower the brightness
import signal
import sys
import time

from openwestkit import OpenWestKit


# signal handler that resets the board when ctrl-c is pressed
def handleSignal(signal, frame):
    openwestkit.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, handleSignal)

openwestkit = OpenWestKit()

openwestkit.reset()
brightness = 65
while(1):
    openwestkit.brightness(brightness)
    time.sleep(1)

    for code in openwestkit.readData():
        if code == 'a':
            brightness -= 5
        elif code == 'b':
            brightness += 5

    # max
    if brightness > 255:
        brightness = 255
    # min
    if brightness < 5:
        brightness = 5

    print 'Brightness:', brightness
