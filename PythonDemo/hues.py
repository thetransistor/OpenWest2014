#!/usr/bin/env python2

"""Cycles through different hues. Speed can be adjusted with the buttons."""
import signal
import sys

from colorsys import hsv_to_rgb
from time import sleep
from openwestkit import OpenWestKit

# Constants: Adjust these to your liking.
#
# These decimals represent the hue of a color. So a value of 1 is one full
# revolution of the color wheel and 0.5 would be half of the color wheel.

# Offset in color between pixels
# Adjust this to get a different color difference betwen the pixels
OFFSET = 0.10

# How much the speed changes when a button is pressed
BUTTON_RATE = 0.01

# How long to sleep before updating the next LED
SPEED = 0.02


def handle_signal(signal, frame):
    """Quit on ctrl-c."""
    sys.exit(0)


def get_rgb(hue=0, pixelNum=0):
    """
    Converts the current hue and pixel number to a color in rgb as a list.
    
    'pixelNum' is used to provide the offset.
    """
    # The value are still in the range [0, 1]
    color = hsv_to_rgb((hue - (OFFSET * pixelNum)) % 1, 1, 1)
    
    # Convert range from [0, 1] to [0, 255]
    return map(lambda x: int(x * 255), color)


def adjust_rate(code, rate):
    """Adjusts the rate by which the pixels change their hue."""
    # 'b' is the left button. 'a' is the right.
    lr = rate + (BUTTON_RATE if code == 'b' else
                 (-BUTTON_RATE if code == 'a' else 0))
    if -0.005 < lr < 0.005:
        lr = 0
    return lr


def init():
    """Returns an OpenWestKit object and makes the brightness tolerable. :)"""
    openwestkit = OpenWestKit()
    openwestkit.brightness(16) #16 doesn't blind me when I stare

    return openwestkit


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_signal)
    openwestkit = init()

    hue = 0
    rate = 0.01
    # Set an out-of-band old rate to trigger a message on first time through
    # event loop.
    oldrate = 100
    while (1):
        # Check for button presses
        for code in openwestkit.readData():
            rate = adjust_rate(code, rate)
            if rate != oldrate:
              oldrate = rate
              print "button rate", rate
            
        for pixelNum in range(0, 4):
            (r, g, b) = get_rgb(hue, pixelNum)
            openwestkit.setPixel(pixelNum, r, g, b)

            sleep(SPEED)

        hue += rate % 1
