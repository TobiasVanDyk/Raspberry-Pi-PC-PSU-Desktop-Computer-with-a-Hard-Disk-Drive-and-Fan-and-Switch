# Raspberry Pi PC PSU Desktop Computer with a Hard Disk Drive and Fan and Switch

<img src="https://github.com/TobiasVanDyk/Raspberry-Pi-PC-PSU-Desktop-Computer-with-a-Hard-Disk-Drive-and-Fan-and-Switch/blob/master/photo-1.jpg" width="600" height="437" />

<img src="https://github.com/TobiasVanDyk/Raspberry-Pi-PC-PSU-Desktop-Computer-with-a-Hard-Disk-Drive-and-Fan-and-Switch/blob/master/photo-2.jpg" width="809" height="582" />

For more details please see the [**Instructables project**](https://www.instructables.com/id/A-Rasberry-Pi-PC-PSU-Desktop-Computer-With-Hard-Di/)

I grew tired of connecting all the peripherals to my Raspberry Pi 3 or 4, every time I wanted to use it. I decided I wanted a Raspberry Pi computer permanently connected to a power supply, hard disk for the root file system and data, a large fan that can rotate slowly and quietly, and a monitor and speakers.

In addition it is not a good idea to run a Pi for an extended period from an SD Card - these have a limited write cycle (about 10,000 times?) and I therefore decided to investigate other ways to run the Pi.

The photo shows the completed Pi case connected to a small monitor, stereo speakers, and a wireless combo-keyboard trackpad, and Hayley Westenra singing Scarborough Fair using the Rasbian and omxplayer's video hardware acceleration.

The Raspberry Pi 3 in some of the older photos was recently replaced with a a Raspberry Pi 4 4GB. The temperature stays between 40 and 50 degrees Celsius. I have tested the Raspberry Pi 4 with an Orico USB 3 enclosure circuit board and it works well - to remove the USB to SATA circuit board unclip the aluminum plate at the top and then you can remove the circuit board after unscrewing two small screws. Details at [**Orico USB 3 Enclosure**](www.orico.co.za/product/orico-usb3-0-2-5-enclosure-blue/)


### Parts List

<img src="https://github.com/TobiasVanDyk/Raspberry-Pi-PC-PSU-Desktop-Computer-with-a-Hard-Disk-Drive-and-Fan-and-Switch/blob/master/photo-3.jpg" width="750" height="719" />

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
<img src="https://github.com/TobiasVanDyk/Raspberry-Pi-PC-PSU-Desktop-Computer-with-a-Hard-Disk-Drive-and-Fan-and-Switch/blob/master/photo-4.jpg" width="831" height="706" />

An old computer PSU case seemed to be a convenient size to house the Pi, its power supply, and a stripped external USB hard disk. There was not enough space in the PSU case to mount the external hdd with its case - I therefore opened it and only kept the small circuit board attached to the hdd. I also added a power switch plus USB sockets on the front and back, and it had space for a large fan to keep everything cool, and I made provision for a DAC hat to be fitted should I acquire one. I used a 12v 3A AC-DC power supply as the main PSU, and added two smaller adjustable 5v and 7v for the fan, DC-DC PSU's.

The photo shows all the components when partially assembled in the PSU case. I made four short USB 2 cables to connect the four Raspberry Pi USB 2 and 3 ports to the hard disk, and the front and back panel usb connectors.

The other photos show the completed Pi case connected to a small monitor, stereo speakers, and a wireless combo keyboard track pad, and the completed case from various angles.

If you look at the last photo carefully you can see that I have connected two wires (brown and white) directly to the raspberry Pi 3 or 4 GPIO pins. In this case the Pi 3 or 4 is powered directly via its GPIO pins 2 or 4 are +5v, pin 6 (and others) for ground - but note that you must triple-check that you are supplying no more than about 5.2 volt to those pins as by doing this you're bypassing the poly-fuse protection. I used Pins 2 for +5v and the pin next to it for Ground. As I am supplying the Pi through two regulated power supplies - first 12v and then 5.1v, I was satisfied with the direct supply connection.

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

Prepare a suitable 2.5" hdd or ssd in either windows or linux (attach the hdd through tan external USB enclosure), by creating two partitions: A small 20GB to 100GB partition which will hold the root file system and a larger partion that fills the rest of the drive which wil be used for user data.

Do not format or mount the partitions - they will both be formatted as ext4.

Attach the HDD/SSD to the Raspberry Pi via a USB to SATA converter or take out the circuit board from a an external USB converter. Make a bootable sd card with newest Raspbian June 2019 image and boot Pi - say CANCEL when new setup procedure shows. 

2. Change config.txt sudo nano /boot/config.txt (Press Ctr-O to save and Ctr-X to exit) by adding at bottom: program_usb_timeout=1
max_usb_current=1

If a DAC is used then also:
Remove the driver for the onboard sound: Remove the line dtparam=audio=on from /boot/config.txt if it exists (can just add # in front)
Also in /boot/config.txt and add the following line: dtoverlay=hifiberry-dacplus

Change config.txt 
sudo nano /boot/config.txt 

(Press Ctr-O to save and Ctr-X to exit) by adding at bottom of config.txt: 
program_usb_timeout=1
max_usb_current=1

Raspbian will mount the attached hdd - unmount both partitions then copy the root file system to the first one:
sudo mke2fs -t ext4 -L rootfs /dev/sda1
sudo mount /dev/sda1 /mnt
df -h
sudo rsync -axv / /mnt

Also format the second partition:
sudo mke2fs -t ext4 -L rootfs /dev/sda2

Edit cmdline.txt to boot the hdd root filesyetem:
sudo cp /boot/cmdline.txt /boot/cmdline.sd
sudo nano /boot/cmdline.txt
Change root=**** to root=/dev/sda1

Change fstab on the mounted hdd:
sudo nano /mnt/etc/fstab
Change /dev/xxxxx / ext4 defaults,noatime 0 1 to
/dev/sda1 / ext4 defaults,noatime 0 1

sudo reboot

After rebooting check again with df -h if /dev/sda1 is now listed as the root /

Now you must do the initial Raspberry Pi setup that was skipped at the start using the Raspberry Pi configuration Tool
from the Settings Menu: Change Password, set Locale, WiFi country, Keyboard, Timezone - you will need to reboot

You can then do updates:
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove

If problem with missing pcakages try to re-run the first 2 commands and also try 
sudo apt-get update --fix-missing 
or 
sudo apt-get dist-upgrade --fix-missing

Now add the second partition as a data drive:
sudo mkdir /mnt/data
sudo chown pi:pi /mnt/data
Add /dev/sda2 /mnt/data ext4 default 0 0 to fstab using nano
sudo nano /mnt/etc/fstab
sudo mount -a
sudo chown pi:pi /mnt/data
df -h
Check if sda2 shows correctly then reboot and check again.


9. If a DAC used create new asound.conf in etc/ (nano /etc/alsa.conf with the following lines:

pcm.!default { type hw card 0 }

ctl.!default { type hw card 0 }

10. Reboot then add DSP and analog sound to sound config in Raspberry Pi setting Make sure main volume click on speaker in panel is not 100% Open a console in sda2 folder with the video then:

If DAC Play with omxplayer: omxplayer -o alsa "File Name.mp4" On normal Pi with BCM audio just open terminal in Music folder and omxplayer name.mp4
Step 6: Raspberry Pi 4 $GB
Picture of Raspberry Pi 4 $GB
Picture of Raspberry Pi 4 $GB
Picture of Raspberry Pi 4 $GB
Picture of Raspberry Pi 4 $GB

I bought a Raspberry Pi 4 4GB and replaced the Raspberry Pi 3 with it in the same enclosure. The temperature stays between 40 and 50 degrees Celsius. I must now obtain a USB 3 HDD or SSD to SATA converter and replace the USB 2 version with that.