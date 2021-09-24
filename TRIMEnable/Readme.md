To enable SSD TRIM in linux for the ASMedia enclosure used in the two photos as above, follow the procedure here [**Enabling TRIM Support on a Via VL817 USB 3.1 SATA Adaptor**](https://spod.cx/blog/enabling_trim_support_via_VL817_usb_sata_adaptor.shtml):
1. **lsusb -t** Check that SSD supports **uas**
2. **sudo apt install sg3-utils** To enable **sg_vpd**
3. **sudo sg_vpd -a /dev/sda** Where sda is the SSD - check if **Unmap command supported (LBPU): 1** is present
4. **lsusb** Check chipset vendor and device id's: **ASMEDIA is 174c:55aa and VIA VL817 is 2109:0715**
5. **sudo nano /etc/udev/rules.d/50-uasp-usb.rules** Add this content and substitute vvvv and dddd with the vendor and device id: ACTION=="add|change", ATTRS{idVendor}=="vvvv", ATTRS{idProduct}=="dddd", SUBSYSTEM=="scsi_disk", ATTR{provisioning_mode}="unmap"
6. **sudo udevadm control --reload-rules && udevadm trigger** Better to reboot anyway
7. **sudo fstrim / --verbose**
Note that I had to update the firmware on the ASMedia SSD enclosures to version **141126_A1_EE_82.bin** using the MPTool.exe before the TRIM command would work. The udev rule files and history for both the ASMedia and VIA chipsets are uploaded here in the TRIMEnable folder.
