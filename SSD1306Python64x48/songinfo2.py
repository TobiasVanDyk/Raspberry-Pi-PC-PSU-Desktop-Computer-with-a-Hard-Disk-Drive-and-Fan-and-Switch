##################################
# Working module
# Adafruit-modified lib preferred
# See scroller.py
#################################
import os
import sys
import time
import subprocess

from demo_opts import get_device
#from luma.core.render import canvas
from PIL import ImageFont

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=64, height=48)

songtitle = subprocess.check_output("audtool current-song-tuple-data title", shell=True)
songartist = subprocess.check_output("audtool current-song-tuple-data artist", shell=True)
songinfo = subprocess.check_output("audtool current-song", shell=True)

print(songinfo)

with canvas(device) as draw:

    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((2, 2), songinfo, fill="white")
    draw.text((2, 16), songtitle, fill="white")
    draw.text((2, 32), songartist, fill="white")
time.sleep(5)

        
        
