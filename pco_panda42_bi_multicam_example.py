import ctypes as C

import pco_panda42_bi

## An example of how to operate 2 pco_panda42_bi USB 3.0 cameras on the same PC:

# Find a way to distinguish them:
# -> The best way would be to get the serial number, but this is hard to
# extract with the complex PCO SDK 'nested structs' (attempts to use these
# gave serial number = 0).
# -> Here it was found that the 'Sensor name' was different between the 2
# panda cameras, so this was used to check identity.
# -> It was also found that the camera order was maintained when requesting a
# handle to the next available camera. So camera identity is preserved by the
# order of handle collection with 'dll.open_camera'.

# NOTE: passing 'handle1' and 'handle2' to init the cameras works fine here,
# but does not work with concurrency tools (error: "ctypes objects containing
# pointers cannot be pickled"). However, since the order is (seemingly)
# preserved, the cameras can be initialized (in order) without collecting
# handles in advance, by simply calling them in the correct order in the usual
# way. So whilst the code here is useful for proving the preservation of order,
# it will not work with concurrency tools.

## code to distinguish the cameras using the 'Sensor name':

get_info_string = pco_panda42_bi.dll.PCO_GetInfoString
get_info_string.argtypes = [
    C.c_void_p,             # ph (Handle to an open camera)
    C.c_uint16,             # dwinfotype (pick camera information to inquire)
    C.c_char_p,             # buf_in (Pointer to 40 byte character array)
    C.c_uint16]             # size_in (Size of array)
get_info_string.restype = pco_panda42_bi.check_error

def get_info(handle, info_type):
    """
    0 = Camera name and interface information.
    1 = Camera name.
    2 = Sensor name.
    3 = Production number.
    """
    dwinfotype = (info_type)
    camera_info_length = 100
    camera_info = C.c_char_p(camera_info_length * b' ')
    get_info_string(handle, dwinfotype, camera_info, camera_info_length)
    print("camera_info %i = %s"%(info_type, camera_info.value))
    return camera_info.value

## test code:
from tifffile import imread, imwrite
for i in range(1): # successfully run to 100 iterations
    # initialize some handles:
    handle1, handle2 = C.c_void_p(0), C.c_void_p(0)
    # try to open some cameras:
    pco_panda42_bi.dll.open_camera(handle1, 0)
    pco_panda42_bi.dll.open_camera(handle2, 0)
    # check that the camera identities are maintained:
    assert get_info(handle1, 2) == b'S021300626 PCB000000000'
    assert get_info(handle2, 2) == b'S021300833 PCB000000000'
    # init the cameras using the prescribed handles:
    camera1 = pco_panda42_bi.Camera(name='PCO.panda4.2_bi_1',
                                    handle=handle1,
                                    verbose=True,
                                    very_verbose=False)
    camera2 = pco_panda42_bi.Camera(name='PCO.panda4.2_bi_2',
                                    handle=handle2,
                                    verbose=True,
                                    very_verbose=False)
    # take some pictures:
    camera1.apply_settings(
        num_images=100, exposure_us=1000, height_px='min', width_px=100)
    images1 = camera1.record_to_memory()
    imwrite('test0_1.tif', images1, imagej=True)
    camera2.apply_settings(
        num_images=100, exposure_us=1000, height_px='min', width_px=100)
    images2 = camera2.record_to_memory()
    imwrite('test0_2.tif', images2, imagej=True)
    # close:
    camera1.close()
    camera2.close()
