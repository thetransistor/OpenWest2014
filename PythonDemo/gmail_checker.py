# Gmail Checker - Glows when you have unread emails
# Click button "a" or "b" to open a browser to first unread email (limited support)
import signal
import sys
import time
import math
import urllib2
import base64
import webbrowser
from xml.dom.minidom import parse, parseString
from openwestkit import OpenWestKit


# signal handler that resets the board when ctrl-c is pressed
def handleSignal(signal, frame):
    openwestkit.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, handleSignal)

openwestkit = OpenWestKit()

# programming logic begins

new_emails = False
# store the first email link
first_entry_link = None

gmail_username = ""
gmail_password = ""
gmail_atom_feed_url = "https://mail.google.com/mail/feed/atom"

global_count = 0

angle_step = .05 # reduce the step to make the glow seq slower
angle = 0
while (1):
    if (new_emails):
        # determine the strength of the pixel as white
        color = int(abs(math.sin(angle) * 155)) # set pixel brightness (max 255)
        openwestkit.setPixel(0, 0, color, 0)
        angle += angle_step
        
        # check for button press to read new emails
        for code in openwestkit.readData():
            if code == 'a' or code == 'b':
                # open browser window
                webbrowser.open(first_entry_link, 2)
    else:
        # no new emails, let's reset the pixel and angle
        openwestkit.setPixel(0, 0, 0, 0)
        angle = 0
    
    # check our global counter (check every 6k iterations or every 1 minute)
    if (global_count % 6000 == 0):
        print ('checking gmail')
        base64string = base64.encodestring('%s:%s' % (gmail_username, gmail_password)).replace('\n', '')
        request = urllib2.Request(gmail_atom_feed_url)
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Content-Type", "application/xml;charset=utf-8")

        try:
            # handle atom feed XML response
            result = urllib2.urlopen(request)
            _xml = parseString(result.read())
            count_node = _xml.getElementsByTagName("fullcount")[0]
            new_count = count_node.childNodes[0].data
            # check the total number of unread messages
            # if greater than 1, set the pixel flag
            if (int(new_count) > 0):
                print ("%s new email(s)!" % new_count)
                new_emails = True
              
                # get the first unread email entry link
                first_entry_node = _xml.getElementsByTagName("entry")[0]
                first_entry_link_node = first_entry_node.getElementsByTagName("link")[0]
                first_entry_link = first_entry_link_node.attributes["href"].value

        except urllib2.URLError, e:
            print e.read()

    global_count += 1
    time.sleep(.001)
