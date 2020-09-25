#!/bin/bash

<<COMMENT
A sequence of shell scripts to 
1. Transfer the root partition to a hdd or ssd and create a data partition
2. Update Raspberry Pi OS
COMMENT

:' 
Keep the Dos Boot Partition on the SD Card and Move the Root and User Files to a Hard Disk or SSD.
Prepare a suitable 2.5" hdd or ssd in either windows or linux (attach the hdd through tan external USB enclosure), 
by creating two partitions: A small 20GB to 100GB partition which will hold the root file system and a larger partion 
that fills the rest of the drive which wil be used for user data.
Do not format or mount the partitions - they will both be formatted as ext4.
Attach the HDD/SSD to the Raspberry Pi via a USB to SATA converter or take out the circuit board from a an external USB converter.
Make a bootable sd card with newest Raspberry Pi Os Aug 2020 image and boot Pi - complete the new setup procedure. 
'

# Change config.txt 
sudo nano /boot/config.txt 

# (Press Ctr-O to save and Ctr-X to exit) by adding at bottom of config.txt: 
# program_usb_timeout=1
# max_usb_current=1

# Raspbian will mount the attached hdd - unmount both partitions then copy the root file system to the first one:
sudo mke2fs -t ext4 -L rootfs /dev/sda1
sudo mount /dev/sda1 /mnt
df -h
sudo rsync -axv / /mnt

# Also format the second partition:
sudo mke2fs -t ext4 -L rootfs /dev/sda2

# Edit cmdline.txt to boot the hdd root filesyetem:
sudo cp /boot/cmdline.txt /boot/cmdline.sd
sudo nano /boot/cmdline.txt
# Change root=**** to root=/dev/sda1

# Change fstab on the mounted hdd:
sudo nano /mnt/etc/fstab
# Change /dev/xxxxx / ext4 defaults,noatime 0 1 to
# /dev/sda1 / ext4 defaults,noatime 0 1

sudo reboot

# After rebooting check again with df -h if /dev/sda1 is now listed as the root /

# You can then do updates:
sudo apt-get update
sudo apt-get full-upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove

# If problem with missing pcakages try to re-run the first 2 commands and also try 
sudo apt-get update --fix-missing 
# or 
sudo apt-get dist-upgrade --fix-missing

# Now add the second partition as a data drive:
sudo mkdir /mnt/data
sudo chown pi:pi /mnt/data
# Add /dev/sda2 /mnt/data ext4 default 0 0 to fstab using nano
sudo nano /mnt/etc/fstab
sudo mount -a
sudo chown pi:pi /mnt/data
df -h
# Check if sda2 shows correctly then reboot and check again.

# All done!

