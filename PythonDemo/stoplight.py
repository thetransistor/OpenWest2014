# A simple traffic light
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

while(1):
    # Green light
    openwestkit.clear()
    openwestkit.setPixel(2, 0, 255, 0)
    time.sleep(3)

    # Yellow light
    openwestkit.clear()
    openwestkit.setPixel(1, 255, 255, 0)
    time.sleep(1)

    # Red light
    openwestkit.clear()
    openwestkit.setPixel(0, 255, 0, 0)
    time.sleep(3)
