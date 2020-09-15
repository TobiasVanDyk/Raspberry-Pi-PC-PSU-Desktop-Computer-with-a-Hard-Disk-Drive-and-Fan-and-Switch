 
# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import logging

import Adafruit_GPIO as GPIO


# Constants
SSD1306_I2C_ADDRESS = 0x3C    # 011110+SA0+RW - 0x3C or 0x3D
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10
SSD1306_SETSTARTLINE = 0x40
SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SEGREMAP = 0xA0
SSD1306_CHARGEPUMP = 0x8D
SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

# Scrolling constants
SSD1306_ACTIVATE_SCROLL = 0x2F
SSD1306_DEACTIVATE_SCROLL = 0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A


class SSD1306Base(object):
    """Base class for SSD1306-based OLED displays.  Implementors should subclass
    and provide an implementation for the _initialize function.
    """

    def __init__(self, width, height, rst, dc=None, sclk=None, din=None, cs=None,
                 gpio=None, spi=None, i2c_bus=None, i2c_address=SSD1306_I2C_ADDRESS,
                 i2c=None):
        #self._log = logging.getLogger('Adafruit_SSD1306.SSD1306Base')
        self._spi = None
        self._i2c = None
        self.width = width
        self.height = height
        self._pages = height//8
        self._buffer = [0]*(width*self._pages)
        # Default to platform GPIO if not provided.
        self._gpio = gpio
        if self._gpio is None:
            self._gpio = GPIO.get_platform_gpio()
        # Setup reset pin.
        self._rst = rst
        if not self._rst is None:
            self._gpio.setup(self._rst, GPIO.OUT)
        # Handle hardware SPI
        if spi is not None:
            #self._log.debug('Using hardware SPI')
            self._spi = spi
            self._spi.set_clock_hz(8000000)
        # Handle software SPI
        elif sclk is not None and din is not None and cs is not None:
            #self._log.debug('Using software SPI')
            self._spi = SPI.BitBang(self._gpio, sclk, din, None, cs)
        # Handle hardware I2C
        elif i2c is not None:
            self._log.debug('Using hardware I2C with custom I2C provider.')
            self._i2c = i2c.get_i2c_device(i2c_address)
        else:
            #self._log.debug('Using hardware I2C with platform I2C provider.')
            import Adafruit_GPIO.I2C as I2C
            if i2c_bus is None:
                self._i2c = I2C.get_i2c_device(i2c_address)
            else:
                self._i2c = I2C.get_i2c_device(i2c_address, busnum=i2c_bus)
        # Initialize DC pin if using SPI.
        if self._spi is not None:
            if dc is None:
                raise ValueError('DC pin must be provided when using SPI.')
            self._dc = dc
            self._gpio.setup(self._dc, GPIO.OUT)

    def _initialize(self):
        raise NotImplementedError

    def command(self, c):
        """Send command byte to display."""
        if self._spi is not None:
            # SPI write.
            self._gpio.set_low(self._dc)
            self._spi.write([c])
        else:
            # I2C write.
            control = 0x00   # Co = 0, DC = 0
            self._i2c.write8(control, c)

    def data(self, c):
        """Send byte of data to display."""
        if self._spi is not None:
            # SPI write.
            self._gpio.set_high(self._dc)
            self._spi.write([c])
        else:
            # I2C write.
            control = 0x40   # Co = 0, DC = 0
            self._i2c.write8(control, c)

    def begin(self, vccstate=SSD1306_SWITCHCAPVCC):
        """Initialize display."""
        # Save vcc state.
        self._vccstate = vccstate
        # Reset and initialize display.
        self.reset()
        self._initialize()
        # Turn on the display.
        self.command(SSD1306_DISPLAYON)

    def reset(self):
        """Reset the display."""
        if self._rst is None:
            return
        # Set reset high for a millisecond.
        self._gpio.set_high(self._rst)
        time.sleep(0.001)
        # Set reset low for 10 milliseconds.
        self._gpio.set_low(self._rst)
        time.sleep(0.010)
        # Set reset high again.
        self._gpio.set_high(self._rst)

    def display(self):
        # mcauser commented on Apr 6, 2016 https://github.com/adafruit/Adafruit_SSD1306/issues/60
        # I have a partially working fork using a 64x48 OLED and a WeMos D1 mini (ESP8266) over hardware SPI.
        # The scrolling example does not work as expected.
        # There are random pixels offscreen.
        # In display() I set the column start address to 32, column end address to 95 and page end address to 5.
        # ssd1306_command(SSD1306_COLUMNADDR);
        # ssd1306_command(32);  // Column start
        # ssd1306_command(95);  // Column end (32+64-1)
        # ssd1306_command(SSD1306_PAGEADDR);
        # ssd1306_command(5);  // Page end ((48/8)-1)
        """Write display buffer to physical display."""
        self.command(SSD1306_COLUMNADDR)
        self.command(32)              # Column start address. (0 = reset)
        self.command(95)              # Column end address.
        self.command(SSD1306_PAGEADDR)
        self.command(0)              # Page start address. (0 = reset)
        self.command(5)              # Page end address.
        # Write buffer data.
        if self._spi is not None:
            # Set DC high for data.
            self._gpio.set_high(self._dc)
            # Write buffer.
            self._spi.write(self._buffer)
        else:
            for i in range(0, len(self._buffer), 16):
                control = 0x40   # Co = 0, DC = 0
                self._i2c.writeList(control, self._buffer[i:i+16])

    def image(self, image):
        """Set buffer to value of Python Imaging Library image.  The image should
        be in 1 bit mode and a size equal to the display size.
        """
        if image.mode != '1':
            raise ValueError('Image must be in mode 1.')
        imwidth, imheight = image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display ({0}x{1}).' \
                .format(self.width, self.height))
        # Grab all the pixels from the image, faster than getpixel.
        pix = image.load()
        # Iterate through the memory pages
        index = 0
        for page in range(self._pages):
            # Iterate through all x axis columns.
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                bits = 0
                # Don't use range here as it's a bit slow
                for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
                    bits = bits << 1
                    bits |= 0 if pix[(x, page*8+7-bit)] == 0 else 1
                # Update buffer byte and increment to next byte.
                self._buffer[index] = bits
                index += 1

    def clear(self):
        """Clear contents of image buffer."""
        self._buffer = [0]*(self.width*self._pages)

    def set_contrast(self, contrast):
        """Sets the contrast of the display.  Contrast should be a value between
        0 and 255."""
        if contrast < 0 or contrast > 255:
            raise ValueError('Contrast must be a value from 0 to 255 (inclusive).')
        self.command(SSD1306_SETCONTRAST)
        self.command(contrast)

    def dim(self, dim):
        """Adjusts contrast to dim the display if dim is True, otherwise sets the
        contrast to normal brightness if dim is False.
        """
        # Assume dim display.
        contrast = 0
        # Adjust contrast based on VCC if not dimming.
        if not dim:
            if self._vccstate == SSD1306_EXTERNALVCC:
                contrast = 0x9F
            else:
                contrast = 0xCF
            self.set_contrast(contrast)

class SSD1306_64_48(SSD1306Base):
    def __init__(self, rst, dc=None, sclk=None, din=None, cs=None, gpio=None,
                 spi=None, i2c_bus=None, i2c_address=SSD1306_I2C_ADDRESS,
                 i2c=None):
        # Call base class constructor.
        super(SSD1306_64_48, self).__init__(64, 48, rst, dc, sclk, din, cs,
                                             gpio, spi, i2c_bus, i2c_address, i2c)

    def _initialize(self):
        # 64x48 pixel specific initialization.
        self.command(SSD1306_DISPLAYOFF)                    # 0xAE
        self.command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        self.command(0x80)                                  ###### the suggested ratio 0x40=64

        self.command(SSD1306_SETMULTIPLEX)                  # 0xA8
        self.command(0x2F)                                  ###### ssd1306_command(SSD1306_LCDHEIGHT - 1) 0x2F=47

        self.command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        self.command(0x0)                                   # no offset
        self.command(SSD1306_SETSTARTLINE | 0x0)            # line #0
        self.command(SSD1306_CHARGEPUMP)                    # 0x8D
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x10)
        else:
            self.command(0x14)
        self.command(SSD1306_MEMORYMODE)                    # 0x20
        self.command(0x00)                                  # 0x0 act like ks0108
        self.command(SSD1306_SEGREMAP | 0x1)
        self.command(SSD1306_COMSCANDEC)

        self.command(SSD1306_SETCOMPINS)                    # 0xDA
        self.command(0x12)                                  ###### was 0x12
        self.command(SSD1306_SETCONTRAST)                   # 0x81
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x9F)
        else:
            self.command(0xCF)
        self.command(SSD1306_SETPRECHARGE)                  # 0xd9
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x22)
        else:
            self.command(0xF1)
        self.command(SSD1306_SETVCOMDETECT)                 # 0xDB
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        self.command(SSD1306_NORMALDISPLAY)                 # 0xA6


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# 64x48 display with hardware I2C:
disp = SSD1306_64_48(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
 
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0,0,width,height), outline=1, fill=1)           # should be width-1 height-1

x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)


while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width-1,height-1), outline=1, fill=0)
    time.sleep(1)

    draw.text((2, 0),       "ABC123",  font=font, fill=255)
    draw.text((2, 12),     "1234567890", font=font, fill=255)

    # Display image.
    disp.dim(True)           # No effect?
    disp.image(image)
    disp.display()
    time.sleep(3)
    # Clear display.
    disp.clear()
    disp.display()
    time.sleep(3)

    songinfo = os.system("audtool current-song")
    songtitle = subprocess.check_output("audtool current-song-tuple-data title", shell=True)
    songartist = subprocess.check_output("audtool current-song-tuple-data artist", shell=True)
    songinfo = subprocess.check_output("audtool current-song", shell=True)

    print(songinfo)
    
    offset = 0
    n = songinfo.len
    while offset<n:
        t = " "
        i = 0
        while i<width:
            t[i] = songinfo[offset+i]
            i += 1
        draw.rectangle((0,0,width-1,height-1), outline=0, fill=0)
        draw.text((0, 2), t, fill="white")
        disp.image(image)
        disp.display()
        offset += 1
        time.sleep(1)

    #draw.text((2, 2), songinfo, fill="white")
    #draw.rectangle((0,0,width-1,height-1), outline=0, fill=0)
    #draw.text((0, 2), songtitle, fill="white")
    #draw.text((0, 12), songartist, fill="white")
    #disp.image(image)
    #disp.display()
    time.sleep(5)
    