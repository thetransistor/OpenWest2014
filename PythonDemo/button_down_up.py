#!/usr/bin/env python
# Indicates which button combination is being held down
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

def inputs(code):
    if code == 'a':
        inputs.button1 = 1
    elif code == 'b':
        inputs.button2 = 1
    elif code == 'A':
        inputs.button1 = 0
    elif code == 'B':
        inputs.button2 = 0

openwestkit = OpenWestKit(debug=True)

inputs.button1 = 0
inputs.button2 = 0
while (1):

    # Pick a random color
    r, g, b = random.randrange(255), random.randrange(255), random.randrange(255)

    time.sleep(0.05)

    for code in openwestkit.readData():
        inputs(code)

    if inputs.button1 == 1:
        openwestkit.setPixel(0, r, g, b)
        openwestkit.setPixel(1, 50, 50, 50)
    else:
        openwestkit.setPixel(1, 0, 0, 0)

    if inputs.button2 == 1:
        openwestkit.setPixel(3, r, g, b)
        openwestkit.setPixel(2, 25, 25, 25)
    else:
        openwestkit.setPixel(2, 0, 0, 0)
