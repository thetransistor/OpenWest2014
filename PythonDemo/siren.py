# Flashing siren, use buttons to enable and disable
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

on = True
while (1):
    if on:
        openwestkit.clear()
        openwestkit.setPixel(0, 0, 0, 255)
        openwestkit.setPixel(3, 0, 0, 255)
        time.sleep(.1)
        openwestkit.clear()
        openwestkit.setPixel(1, 255, 0, 0)
        openwestkit.setPixel(2, 255, 0, 0)
        time.sleep(.1)

    for code in openwestkit.readData():
        if code == 'a':
            on = False
            for pos in range(0, 4):
                openwestkit.setPixel(pos, 0, 0, 0)
        elif code == 'b':
            on = True
