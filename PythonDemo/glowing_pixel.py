# Fading lights - use buttons to enable and disable
import signal
import sys
import time
import math

from openwestkit import OpenWestKit


# signal handler that resets the board when ctrl-c is pressed
def handleSignal(signal, frame):
    openwestkit.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, handleSignal)

openwestkit = OpenWestKit()

# programming logic begins
angle_step = .05 # reduce the step to make the glow seq slower
angle = 0
while (1):
    # determine the strength of the pixel as white
    color = int(abs(math.sin(angle) * 155)) # set pixel brightness (max 255)
    openwestkit.setPixel(0, color, 0, 0)
    time.sleep(.001)
    angle += angle_step    
