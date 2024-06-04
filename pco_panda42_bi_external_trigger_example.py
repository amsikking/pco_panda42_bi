import numpy as np
from tifffile import imread, imwrite
import pco_panda42_bi
import ni_PCI_6733

'''Test the camera's ability to follow external triggers'''
ao = ni_PCI_6733.DAQ(num_channels=1, rate=1e6, verbose=False)

camera = pco_panda42_bi.Camera(verbose=True)
frames = 1000
camera.apply_settings(frames, 100, 'min', 'max', 'binary+ASCII')

jitter_time_us = 1000 # how much slop is needed between triggers? 1000us?
jitter_px = max(ao.s2p(1e-6 * jitter_time_us), 1)
rolling_px = ao.s2p(1e-6 * camera.rolling_time_us)
exposure_px = ao.s2p(1e-6 * camera.exposure_us)
period_px = max(rolling_px, exposure_px) + jitter_px

voltage_series = []
for i in range(frames):
    volt_period = np.zeros((period_px, ao.num_channels), 'float64')
    volt_period[:rolling_px, 0] = 5 # (falling edge is time for laser on!)
    voltage_series.append(volt_period)
voltages = np.concatenate(voltage_series, axis=0)

# can the camera keep up?
ao._write_voltages(voltages) # write voltages first to avoid delay
images = np.zeros( # allocate memory to pass in
    (camera.num_images, camera.height_px, camera.width_px),'uint16')

for i in range(2):
    ao.play_voltages(block=False) # race condition!
    camera.record_to_memory( # -> waits for trigger
        allocated_memory=images, software_trigger=False)
imwrite('test_external_trigger.tif', images, imagej=True)

time_s = ao.p2s(voltages.shape[0])
fps = frames /  time_s
print('fps = %02f'%fps) # (forced by ao play)

camera.close()
ao.close()
