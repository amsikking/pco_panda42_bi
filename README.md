# pco_panda42_bi
Python device adaptor: PCO.panda 4.2 bi USB sCMOS camera.
## Quick start:
- Install the PCO USB interface driver, then install 'Camware' to test the camera and get the latest
 "SC2_Cam.dll" (a version included here). Put the .dll in the directory with "pco_panda42_bi.py" and run
 the script (requires Python and numpy).

![social_preview](https://github.com/amsikking/pco_panda42_bi/blob/main/social_preview.png)

## Details:
- The adaptor reveals a minimal API from the extensive PCO SDK by following the 'typical implementation'
for a series of .dll calls for camera setup, image acquisition and tidy up.
- See the '\_\_main__' block at the bottom of "pco_panda42_bi.py" for some typical ways to interact with a
stand alone camera or "pco_panda42_bi_external_trigger_example.py" for an example of high speed external
triggering (a very useful mode for ultra fast synchronization in a multi-device/microscope system).

**Note:** the camera tested here came a USB-C connector, cable and PCIe adaptor card (SuperSpeed USB 10Gbps PCI Express x4 Card). Windows will typically install a generic driver for this kind of card. However, in this case, the generic windows driver did not work with either Camware or "pco_panda42_bi.py" (buffer timeout error in both cases). The fix was to use the 'update driver' option in windows device manager to point to the specific driver for the exact card (in this case it was the 'Asmedia ASM3142' chipset driver that came on the provided CD).
