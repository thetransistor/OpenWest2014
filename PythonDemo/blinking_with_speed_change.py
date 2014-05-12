# Blinks each LED with a random color, use the buttons to decrease and
# increase the speed of the blinking
import random
import signal
import sys
import time

from openwestkit import OpenWestKit


# signal handler that resets the board when ctrl-c is pressed
def handleSignal(signal, frame):
    openwestkit.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, handleSignal)


def changeSpeed(code, speed):
    if code == 'a':  # button 1 was pressed, speed up
        speed -= .05
    elif code == 'b':  # button 2 was pressed, slow down
        speed += .05

    # Safety check as we can't sleep for less than zero time
    if speed <= 0:
        speed = .05

    return speed

openwestkit = OpenWestKit(debug=True)

speed = 1
while (1):
    for pixelNum in range(0, 4):

        # Pick a random color
        r, g, b = random.randrange(255), random.randrange(255), random.randrange(255)

        openwestkit.setPixel(pixelNum, r, g, b)
        for code in openwestkit.readData():
            speed = changeSpeed(code, speed)

        print "Current speed", speed

        time.sleep(speed)

        openwestkit.setPixel(pixelNum, 0, 0, 0)
        for code in openwestkit.readData():
            speed = changeSpeed(code, speed)
