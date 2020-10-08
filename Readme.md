# Raspberry Pi PC PSU Desktop Computer with a Hard Disk Drive and Fan and Switch

<p align="center">
<img src="images/topfanfinal1.jpg" width="420" />  
<img src="images/m2ssd1.jpg" width="395" />     
</p>

A second Raspberry Pi housed inside a PC power supply case had been built. This uses a fan on top - and the arrangement of the components inside the PC-PSU case is therefore different. A modified (for 64x48 pixels), [**Adafruit SSD1306 driver**](https://github.com/adafruit/Adafruit_Python_SSD1306) or [**Luma Oled for Python**](https://github.com/rm-hull/luma.oled) will be used to display the song or video information on a [**small OLED display**](https://www.robotics.org.za/D1-OLED?search=%20oled) mounted in the front of the case. For the Luma driver refer to [**songinfo2.py**](SSD1306Python64x48/songinfo2.py) inside the SSD1306Python64x48 folder here. The smaller, modified Adafruit SSD1306 library will be used for future development.

A Raspberry Pi 4B is connected to three storage devices: (1) the original 32GB sdcard that now only serves as a boot partition, (2) a 240GB M.2 Western Digital SSD connected through an M.2 to USB3 adapter card - [**NexStar SX M.2 SSD to USB 3.0 Enclosure**](https://www.vantecusa.com/products_detail.php?p_id=214), and (3) a 1TB 2.5" Toshiba hdd connected through a SATA to USBC converter - [**ORICO 2.5 inch Transparent Type-C Hard Drive Enclosure**](http://my.orico.cc/goods.php?id=6352). The M.2 to USB3 converter use an ASMedia chipset (lsusb ID 174c:55aa ASMedia), which should mean it will do UAS without errors - or maybe not: refer to [**this bugzilla.redhat snippet from Hans de Goede about 5 years ago**](ASMedia-usb3-to-sata-bridges-quirks.txt). It is the same [**Hans de Goede**](https://github.com/TobiasVanDyk/gkrellm-uguru-for-GKrellM2) mentioned here regarding 2005 Abit uguru motherboard drivers for lmsensors. SATA to USB3 chipsets that have broken UAS support (which is essential for SSD TRIM operations), can often be partially (a) corrected by keeping them in the Raspberry Pi 4B USB3 hub but then only using the two USB2 data lines, as compared to when using them in the Raspberry Pi 4B USB2 hub. (a): This is then at a big loss in throughput.

Only the Orico interface HDD/SSD SATA-to-USB-C PCB (using a VIA VL817 SATA Adaptor chipset as bridge - lsusb ID 2109:0715 VIA Labs), is used from the enclosure - the plastic case is not used because of better cooling without it. For similar reasons the SSD M.2 adapter is also used without its case. The hdd is currently only connected to the Pi through the USB3 hub D+ and D- USB2 data lines, and it gets its power directly from the output of the 5.1v buck converter that also feeds the Raspberry Pi. `The reason for the direct 5v power connection was that the Raspberry Pi on shutdown removes Vusb without first spinning the hdd down, and as a result a very loud audible "clunk" (hdd emergency retract command on power loss), was heard from the hdd when the Pi is shutting down. When the hdd receives 5v power independent from the Pi, the SATA to USB interface card spins the hdd down after all data signal activity is removed, and no audible retract sound is heard when the Pi is shutting down, nor when the power is switched off from the front panel after the Pi shutdown.` In addition the hdd also does not take any power from the Pi Vusb. Once a short enough USB-C to USB3-A cable is obtained/made the hdd will be interfaced at full USB3 speed. The M.2 Western Digital SSD is powered from the Raspberry Pi's USB3 port - a future upgrade will add another 12v to 5v 3A buck regulator to power all the 5v peripherals. The primary (connected to AC mains) 12v PSU is 36W.

Smartmontools is useed to check the condition od the attached SSD/HDD and hdparm is used to get an indication of the (read) speed. For the first use: `sudo smartctl -a /dev/sdx -d sat` if the normal `sudo smartctl -a /dev/sdx` indicates an unsupported interface. `hdparm -t /dev/sdx1` is used for the read speed indication.

The small sdcard boot partition is used to select through the boot partition's cmdline.txt, which ssd (sda1 or sda2), or hdd (sdb1 or sdb2), root partition to boot. Each of the SSD/HDD drives has two 50GB root partitions and the rest of the space is a data partition (sda3 and sdb3), on each. The two root partitions on the hdd is a mirror (backup) of each of the two ssd root partitions. Fstab is modified for ssd use by adding noatime,nodiratime to the ssd partitions mounted.

`A common problem when using mutiple storage devices is that pcmanfm consumes 25% of the cpu (or 100% of one of four cores), even when the computer is idle.` Compare htop in the first and second picture below. This only happens when the root filesystem is on a hdd or an ssd - not when it is on a SDCard. When the boot partition is on an SDCard and the root partition on a hdd or ssd then the excessive cpu usage is observed. [**Many solutions have been suggested**](pcmanfm-high-cpu.txt), and some work for a limited time such as removing the @ in front of the pcmanfm in /etc/xdg/lxsession/LXDE-pi/autostart, using a local autostart, keeping an sdcard in the slot, etc. What worked for me on two different Raspberry Pi 4Bs with both SSD and HDD storage, is to edit the volume and removable disk mount preferences for the file manager, as shown below in the third picture. 

<p align="center">
<img src="images/pcmanfm3.jpg" width="250" /> 
<img src="images/pcmanfm2.jpg" width="250" />  
<img src="images/pcmanfm1.jpg" width="250" /> 
</p>
<br>

`Because the USB-C port on the Rapsberry Pi 4B is now not used for power, it can be used either in host-mode (i.e. used for keyboards, mice, flash drives or external hdd), or in device-mode (i.e. OTG or gadget mode).` In this case the USB C port was configured for USB-C host mode by adding `dtoverlay=dwc2,dr_mode=host` to /boot/config.txt. It was tested successfully by mounting a 1TB notebook drive using a USB-C to USB-A micro cable.

The i2s audio hat is the [**Wolfson WM8960**](https://www.robotics.org.za/W15668?search=audio%20hat) as discussed in [**other repositories**](https://github.com/TobiasVanDyk/RaspberryPi-GPIO-Audio) here. It is connected to a front panel headphone socket, and a rear panel line out. The separate stereo Class D speaker outputs is also available on the rear panel. 

The SSD1306 display - [**D1 ESP8266 OLED Shield**](https://www.robotics.org.za/D1-OLED) - on the front panel uses i2c for communication and therefore a four-wire ribbon cable is sufficient to connect it to the Raspberry Pi GPIO connector (Pins SCL, SDA, 3V3 and GND). A modified python driver for SSD1306 in its 64x48 pixel version is functional after adapting an Adafruit library based on comments from Mike Causer (modified display: SSD1306_COLUMNADDR, SSD1306_PAGEADDR), and Luma Oled driver (modified SETDISPLAYCLOCKDIV, SETMULTIPLEX, SETCOMPINS. This display was used because of its small physical size but if the size of the front panel opening is not a consideration it will be easier to use a slightly larger, standard 128x64 or 128x32 OLED display. In that case the unmodified Adafruit SSD1306 python driver library can be used. 

To install the [**requirements**](https://github.com/adafruit/Adafruit_Python_GPIO) for the modified driver copy Adafruit_Python_GPIO (which is inside the SSD1306Python64x48 folder here), anywhere under /home/pi, and then run sudo python3 setup.py install from within the folder. The much smaller modified SSD1306 driver is not separate, and is part of the scroller module (scroller123..9.py).

As an example of the SSD1306 python driver refer to [**scroller.py**](SSD1306Python64x48/scroller.py) - this will scroll the current song in audacious (via audtool). The Raspberry Pi CPU temperature is displayed on the second line of the display. To have it start on boot add it as the last line in .bashrc. For example: python3 /home/pi/shared/scroller.py - python 3 is required.

The three M.2 SATA SSD to USB adapters that have been used with a Raspberry Pi 4B are as shown in the table below and in the three pictures left to right:

| Manufacturer | Chipset         | USB VID:PID | Cable Interface | Name and Link                                   |
|:-------------|:----------------|:------------|:----------------|:------------------------------------------------|
| Vantec       | ASMedia ASM1153 | 174c : 55aa | USB 3.0 Micro B | [NexStar SX NST-M2STS3-BK](https://www.vantecusa.com/products_detail.php?p_id=214) |
| Boabab       | JMicro JMS578   | 152d : 0578 | USB 3.0 Micro B | [Baobab M.2 NGFF To USB3.0 Enclosure](https://baobabit.co.za/index.php?route=product/product&path=249&product_id=455) |	       
| Unitek       | VIA VL817       | 2109 : 0715 | USB C           | [Unitek M.2 SSD (NGFF/SATA) Aluminium Enclosure](https://www.unitek-products.com/products/usb3-0-m-2-ssd-ngff-sata-aluminium-enclosure) | 

<p align="center">
<img src="images/Vantec.jpg" width="250" /> 
<img src="images/Baobab.jpeg" width="250" /> 
<img src="images/Unitek.jpg" width="250" />   
</p>

The ASmedia ASM1153 and VIA VL817 both work at full USB 3 speed with UAS enabled, whilst the JMicro JMS578 needs a [quirks entry in cmdline.txt](https://www.raspberrypi.org/forums/viewtopic.php?p=1494113#p1494113) to disable UAS. For more information see [Raspberry Pi 4 USB Boot Config Guide for SSD / Flash Drives](https://jamesachambers.com/raspberry-pi-4-usb-boot-config-guide-for-ssd-flash-drives/). Also refre to [this is a list of the Raspberry Pi Forum posts](RaspberryPi-USB-SSD-Boot.txt) about USB SSD/HDD boot problems and solutions.

*Todo: A persistent third line of the display will be used to show the Raspberry Pi 5 volt supply voltage using either an ATtiny85 as ADC - communicating via i2c with the Raspberry Pi, or an MCP3002 dual channel 10-bit SPI ADC. Both the second and third lines will be on for 1 second out of 5 to prevent OLED burn-in. Remove the need to import the may deprecated Adafruit Github libraries such as Adafruit_GPIO and Adafruit_BBIO etc.*

<p align="center">
<img src="images/topfanfinal4.jpg" width="250" /> 
<img src="images/topfanfinal3.jpg" width="250" /> 
<img src="images/newrpipc1.jpg" width="250" />   
</p>

<p align="center">
<img src="images/newrpipc2.jpg" width="200" /> 
<img src="images/newrpipc3.jpg" width="200" />  
<img src="images/topfanfinal2.jpg" width="200" />  
<img src="images/newrpipc4.jpg" width="200" /> 
</p>

<p align="center">
<img src="images/newrpipc5.jpg" width="250" /> 
<img src="images/m2ssd2.jpg" width="250" /> 
<img src="images/OricoUSBCEnclosure.jpg" width="250" />  
</p>

### Previous build 2018
I grew tired of connecting all the peripherals to my Raspberry Pi 3 or 4, every time I wanted to use it. I decided I wanted a Raspberry Pi computer permanently connected to a power supply, hard disk for the root file system and data, a large fan that can rotate slowly and quietly, and a monitor and speakers. Recently I also added a PiFi DAC (PCM5122) - there is space above the Pi and below the hdd or ssd for this type of hat. See the section at the end for configuration details for this DAC.

In addition it is not a good idea to run a Pi for an extended period from an SD Card - these have a limited write cycle (about 10,000 times?) and I therefore decided to investigate other ways to run the Pi.

The photos shows the completed Pi case connected to a small monitor, stereo speakers, and a wireless combo-keyboard trackpad, and Hayley Westenra singing Scarborough Fair using the Rasbian and omxplayer's video hardware acceleration. I later added a PCM5122 DAC Hat (see picture below), and the four photos below show the result.

For more details please refer to the two [**Instructables project 1**](https://www.instructables.com/id/A-Rasberry-Pi-PC-PSU-Desktop-Computer-With-Hard-Di/) or [**Instructables project 2**](https://www.instructables.com/id/Raspberry-Pi-DAC-Hat-Case-From-PVC-Wall-Box/)

<p align="left">
<img src="images/DACOn1.jpg" width="400" />  
<img src="images/DACOn2.jpg" width="350" /> 
<br>
 
<p align="left">
<img src="images/DACBack1.jpg" width="350" />  
<img src="images/DACInsideOff1.jpg" width="400" /> 
<br>
 
I bought a Raspberry Pi 4 4GB and replaced the Raspberry Pi 3 with it in the same enclosure. The temperature stays between 40 and 50 degrees Celsius even under heavy CPU load conditions. I also acquired two different USB 3 HDD/SSD to SATA converters, and replaced the USB 2 version with that for testing purposes.

Firstly I tested the Raspberry Pi 4 with an Orico USB 3 enclosure circuit board and it works well - to remove the circuit board unclip the aluminum plate at the top and then you can remove the circuit board after unscrewing two small screws. A 10 cm long connection cable is looped once underneath the hard disk  inside the PSU case which keeps it out of the way. 

Secondly I tested a 5cm long open USB3 to SATA converter (please see picture), which also worked well but the shorter cable was too stiff to force it all the way inside the PSU case.

[**Orico USB 3 Enclosure**](https://www.orico.co.za/product/orico-usb3-0-2-5-enclosure-blue/) and **PCM5122 DAC**:
<p align="left">
<img src="images/SATAUSB31.jpg" width="250" />  
<img src="images/PCM5122.jpg" width="250" /> 
</p>

Using a USB 3 interface did result in faster boot and response times (such as when opening the Chromium browser or LibreOffice Writer, but it was not overwhelmingly faster. In addition the Raspberry Pi 3 and 4, supply a maximum of 1.2A spread over all 4 USB 2 and USB 3 ports, which is significantly less than the USB 3 standard. I will therefore remove the power connection on the front USB interface and connect it to a second identical variable 5v power supply module. This will enable me to run another HDD from the front USB interface.

### Parts List

<p align="left">
<img src="images/photo-3.jpg" width="550" />  
<br>
 
* Raspberry Pi 3 or 4
* AC-DC PSU 12v 3A module
* DC-DC PSU module Input 5 to 35v Output 5v 3A
* DC-DC PSU module Input 5 to 35v Output 1A and voltage variable (set to about 7v for a fan speed of 900 rpm)
* One AC 250v pushbutton latching switch
* Three USB female sockets
* Three USB male plugs
* One USB Mini Male Plug
* 3 Digit Voltmeter Blue
* Old PSU case
* Hard Disk Drive or SSD of suitable size (2.5")
* Circuit board from external 2.5" HDD
* 12 volt computer Fan
* Connection wire etc.

### Construction and Connections
<p align="left">
<img src="images/photo-4.jpg" width="550" />  
<br>

An old computer PSU case seemed to be a convenient size to house the Pi, its power supply, and a stripped external USB hard disk. There was not enough space in the PSU case to mount the external hdd with its case - I therefore opened it and only kept the small circuit board attached to the hdd. I also added a power switch plus USB sockets on the front and back, and it had space for a large fan to keep everything cool, and I made provision for a DAC hat to be fitted should I acquire one. I used a 12v 3A AC-DC power supply as the main PSU, and added two smaller adjustable 5v and 7v for the fan, DC-DC PSU's.

The photo shows all the components when partially assembled in the PSU case. I made four short USB 2 cables to connect the four Raspberry Pi USB 2 and 3 ports to the hard disk, and the front and back panel usb connectors.

The other photos show the completed Pi case connected to a small monitor, stereo speakers, and a wireless combo keyboard track pad, and the completed case from various angles.

<p align="left">
<img src="images/photo-12.jpg" width="550" />  
<br>

If you look at the photo above you can see that I have connected two wires (brown and white) directly to the raspberry Pi 3 or 4 GPIO pins. In this case the Pi 3 or 4 is powered directly via its GPIO pins 2 or 4 are +5v, pin 6 (and others) for ground - but note that you must triple-check that you are supplying no more than about 5.2 volt to those pins as by doing this you're bypassing the poly-fuse protection. I used Pins 2 for +5v and the pin next to it for Ground. As I am supplying the Pi through two regulated power supplies - first 12v and then 5.1v, I was satisfied with the direct supply connection.

The new Pi case use a better connection to the GPIO connector with two female headers - see the three photos below:

<p align="center">
<img src="images/GPIOConnect1.jpg" width="250" />  
<img src="images/GPIOConnect2.jpg" width="250" /> 
<img src="images/GPIOConnect3.jpg" width="250" />  
</p>

I was worried that the metal case would block the Raspberry Pi's ability to connect to my Wi-Fi router - in the end I made two 2 cm holes on the side panel next to the Pi board with the result that the number of bars on the Wi-Fi indicator on Raspbian stayed the same whether the case was closed or open.

### Connection Details:

Connect the AC power to the 12v 3A AC-DC Module through the Power switch . Connect the 12v output of this module to the DC-DC 5v 3A module which will power the Raspberry Pi (if adjustable first set to about 5.1 volt - measure it) and to the smaller DC-DC adjustable module which will power the fan. Connect the 5v output of the 5v DC-DC module to the Raspberry Pi GPIO Pins 4 (+5v) and Pin 6 (Ground). Connect the ouput of the smaller DC-DC module to the 12v fan and adjust its output so that the fan turns silently. Connect the ground of the 5v 3A DC-DC module to the PC PSU case. Connect the ground and 5v of the 5v DC-DC module to the 3 digit voltmeter display on the front panel.

Connect two of the Raspberry PI USB ports to the back USB sockets using the two male USB plugs, 4 core wiring and the two USB Female sockets mounted on the rear. Connect one of the Raspberry PI USB ports to the front USB socket using a male USB plug, 4 core wiring and the one USB Female socket mounted on the front.

Connect the hard disk to one of the Raspberry PI USB ports via a male USB plus and another mini USB male plug, or use a USB cable if you have a USB 3 to SATA circuit board available.

### Hard Drive Boot Setup

It is not a good idea to run a Pi for an extended period from an SD Card - these have a limited write cycle (about 10,000 times?) and I therefore decided to leave the small 50 MB Dos boot partition on the SD card (it a read-only during boot), and moving the root file system and user data to a hard disk.

It was very easy to get the Pi to boot from the hard disk - I copied the newest Raspian to an SD card using the Win32DiskImager utility. 

For the Raspberry Pi 3 set the Pi's boot fuse as described below:
Add the line program_usb_boot_mode=1 to /boot/config.txt:
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
This adds program_usb_boot_mode=1 to the end of /boot/config.txt. Reboot the Raspberry Pi. 
Check that the OTP has been programmed with:
vcgencmd otp_dump | grep 17:
Ensure the output 17:0x3020000a is shown which means that the OTP fuse has been successfully programmed.
You can also add the program_usb_boot_mode line from config.txt the nano editor using the command sudo nano /boot/config.txt.

There are two text configuration files (config.txt and cmdline.txt), in the boot folder on the Dos boot partition that one can edit in an attempt to supply either extra power to the hard disk during boot, or to wait longer for the disk to start spinning.

Add: rootdelay=5, and program_usb_timeout=1 and max_usb_current=1 to the long list in the /boot/config.txt file. (The rootdelay option may be deprecated).

Add: boot_delay=1 and again rootdelay=5 to the line in /boot/cmdline.txt should make the kernel wait for the root device before continuing the boot sequence. (Adding rootwait instead of rootdelay will mean it will wait indefinitely.)

### Shell Scripting Source

Note: Please refer to BootHDD.sh

Keep the Dos Boot Partition on the SD Card and Move the Root and User Files to a Hard Disk or SSD.

Prepare a suitable 2.5" hdd or ssd in either windows or linux (attach the hdd/ssd through an external SATA or M.2 to USB enclosure), by creating two partitions: A small 20GB to 100GB partition which will hold the root file system and a larger partion that fills the rest of the drive which wil be used for user data.

Do not format or mount the partitions - they will both be formatted as ext4, or the data partition can be formatted as FAT32.

Attach the HDD/SSD to the Raspberry Pi via the USB to SATA converter or use the circuit board from a an external USB converter. Make a bootable sd card with newest Raspberry Pi OS Aug 2020 image and boot the Pi - complete the setup procedure and reboot. 

Change config.txt<br>
sudo nano /boot/config.txt by adding at bottom:<br>
program_usb_timeout=1<br>
max_usb_current=1

Raspbian will mount the attached hdd - unmount both partitions then copy the root file system to the first one:
```
sudo mke2fs -t ext4 -L rootfs /dev/sda1
sudo mount /dev/sda1 /mnt
df -h
sudo rsync -axv / /mnt
```

Also format the second partition:
```
sudo mke2fs -t ext4 -L rootfs /dev/sda2
```

Edit cmdline.txt to boot the hdd root filesyetem:
```
sudo cp /boot/cmdline.txt /boot/cmdline.sd 
sudo nano /boot/cmdline.txt 
```
Change root=**** to root=/dev/sda1

Change fstab on the mounted hdd:
```
sudo nano /mnt/etc/fstab
```
Change /dev/xxxxx / ext4 defaults,noatime 0 1 to
/dev/sda1 / ext4 defaults,noatime 0 1
```
sudo reboot
```
After rebooting check again with df -h if /dev/sda1 is now listed as the root /

You can then do updates if not done at setup:
```
sudo apt-get update 
sudo apt-get full-upgrade -y 
sudo apt-get dist-upgrade -y 
sudo apt-get autoremove
sudo apt-get autoclean
```

If problem with missing pcakages try to re-run the first 2 commands and also try 
```
sudo apt-get update --fix-missing 
or 
sudo apt-get dist-upgrade --fix-missing
```

Now add the second partition as a data drive:
```
sudo mkdir /mnt/data
sudo chown pi:pi /mnt/data
```
Add /dev/sda2 /mnt/data ext4 default 0 0 to fstab using nano
```
sudo nano /mnt/etc/fstab 
sudo mount -a 
sudo chown pi:pi /mnt/data 
df -h 
```
Check if sda2 shows correctly then reboot and check again.


If a DAC used create new asound.conf in etc/ (nano /etc/alsa.conf with the following lines:

pcm.!default { type hw card 0 }

ctl.!default { type hw card 0 }

Reboot then add DSP and analog sound to sound config in Raspberry Pi setting:
 
Remove the driver for the onboard sound: Remove the line dtparam=audio=on from /boot/config.txt if it exists (can just add # in front). 
Also in /boot/config.txt add the following line: dtoverlay=hifiberry-dacplus

Make sure main volume click on speaker in panel is not 100% Open a console in sda2 folder with the video then:

If DAC Play with omxplayer: omxplayer -o alsa "File Name.mp4" On normal Pi with BCM audio just open terminal in Music folder and omxplayer name.mp4

<p align="center">
<img src="images/photo-5.jpg" width="400" />  
<img src="images/photo-6.jpg" width="400" />  
</p>

<p align="center">
<img src="images/photo-7.jpg" width="400" />  
<img src="images/photo-8.jpg" width="400" />  
</p>

<p align="center">
<img src="images/photo-9.jpg" width="320" />  
<img src="images/photo-10.jpg" width="320" />  
<img src="images/photo-11.jpg" width="320" />  
</p>

In another build, I used an inexpensive Wall Light Switch Box as a Raspberry Pi and DAC Hat Case with space to include a Power Switch as well.

The Raspberry Pi 3 has a board dimension of 56mm wide and 85mm long and I recently discovered that my PiFi Plus DAC hat and the Raspberry Pi will fit into an inexpensive (less than $ 0.50) PVC plastic electrical household wall box used to mount light switches - the one I bought had an outside dimension of 105mm x 60mm x 45mm, and on the inside it was 56mm wide and 101mm long - this means the Pi board will fit (tightly).

The PiFiDAC+ can be obtained from itead.cc or from banggood or from seeedstudio.com for about $6 to $35.

I used a Dremel wheel to cut out the larger rectangular openings, and a step-drill to make the larger round openings - PVC is very easy to drill, cut, file, sand and glue.

I included a power switch for the Pi on the front panel - this is directly connected (soldered on the bottom of the Pi's pcboard), to GPIO pin 4 (+5v). This and a wire from GPIO pin 6 (Ground) is then soldered to a normal power barrel connector mounted on the back panel.

This socket can be used in one of two ways:

1. Use the normal Pi micro-USB connector to supply power to the Pi - the barrel connector will then output +5v to for example a notebook hard disk power supply.

2. Use the barrel connector to supply power to the Pi directly.

The case has a large round opening on the side opposite to the four USB connectors. This is used for ventilation, and also as a window to the Pi's two status lights (red and green), but most importantly the Pi's SD card can be removed and inserted through this hole using a tweezer.

The ventilation seems to be adequate without a fan or a heatsink for the Pi - after an hour of playing flac and mp3 files the CPU temperature varied between 49 and 51 degrees Celsius. There is space to fit a small fan underneath the top cover in the section above the Pi's USB connectors - a fan such as those used for hdd coolers would be suitable and some will operate silently if powered from 5 volt instead of 12 volt.

I intend to use this Pi DAC Box with a 1 TB notebook drive to play music through my stereo amplifier and I must still configure VNC on the Pi and VNC Viewer on a PC, so that I can use the Pi headless from a Windows PC to play music.

I recently upgraded the Pi in the DAC box to the Pi 3B+ and I decided it should now occupy a permanent place in my living room as an audio file player. I used Audacious as the Audio player on the Pi

I partitioned the 1TB hard disk into two partitions - a 50GB partition for the raspberry pi root file system and the rest as a FAT32 partition which holds all the audio files. Doing it this way enables me to plug the hdd into a windows computer and then synchronize it with my music collection on the windows computer. I still use the SD card on the Pi but only as the boot partition - which is read-only and unlikely to be corrupted should there be a power failure.

Windows has a remote desktop client-server built-in already - mstsc.exe or the Remote Desktop Connection.

On the pi side you must install xrdp as shown below:

(1) Install xrdp:<br>
sudo apt-get install xrdp<br>
sudo reboot

Test if xrdp works by:<br>
sudo xrdp

If it ssys it is already running then proceed to the windows computer setup else you will have to remove RealVNC as there is a clash with it and xrdp:

(2) Optional: Remove RealVNC:

sudo apt-get purge realvnc-vnc-server

sudo reboot

and check again if xrdp is now running

(3) If you are running a WiFi connection on the Pi hoover your mouse pointer over the WiFi symbol and write down the wlan ip address such as 192.168.8.102 for example

You can also run:

ifconfig wlan0

on the raspberry pi

If you want to know the raspberry pi's ip address from the windows computer you can run:

nslookup raspberrypi

from the windows command prompt - note that the windows computer and the raspberry must be connected to the same network

(4) On the windows computer right-click on your desktop and choose new shortcut and enter mstsc.exe and name it Remote Desktop. Then open it and for the computer name enter the ip address for the pi and in the second box enter the username pi

It will then connect and ask your for the pi's password.

Then you can open audacious and play you music from your windows computer through the Pi.

To shutdown the pi use:

sudo shutdown


The Pi is mounted on four short 5mm spacers. The top of the wall box was made from a sheet of thin 0.9mm white ABS plastic which can be easily cut and drilled. Please refer to the series of photos for more details on how to mount the Pi and its DAC hat.

The PiFi DAC+ is an inexpensive substitute for the HiFi Berry Pi DAC+ Hat and can be configured in exactly the same way on the Raspberry Pi running Raspbian Stretch - replace the line dtparam=audio=on from /boot/config.txt if with dtoverlay=hifiberry-dacplus. 

<p align="center">
<img src="images/p0.jpg" width="400" />  
<img src="images/p1.jpg" width="400" />  
</p>

<p align="center">
<img src="images/p2.jpg" width="400" />  
<img src="images/p7.jpg" width="400" />  
</p>



