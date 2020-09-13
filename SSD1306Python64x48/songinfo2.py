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

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute parallel(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial, width=64, height=48)
#device.height = 48
#device.width = 64

#songinfo = os.system("audtool current-song")
songtitle = subprocess.check_output("audtool current-song-tuple-data title", shell=True)
songartist = subprocess.check_output("audtool current-song-tuple-data artist", shell=True)
songinfo = subprocess.check_output("audtool current-song", shell=True)

print(songinfo)

song ="ABC"



with canvas(device) as draw:

    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((2, 2), songinfo, fill="white")
    draw.text((2, 16), songtitle, fill="white")
    draw.text((2, 32), songartist, fill="white")
time.sleep(5)

        
        