#!/usr/bin/env python3

#Vision Werver for 2019 Deep Space
# From FRC Team 2877

import cv2
from networktables.util import ntproperty

from visionserver import VisionServer, main
from genericfinder import GenericFinder
from rrtargetfinder2019 import RRTargetFinder2019
# from hatchfinder2019 import HatchFinder2019
# from linefinder2019 import LineFinder2019


class VisionServer2019(VisionServer):

    # Retro-reflective targer finding parameters

    # Color threshold values, in HSV space
    # Original source ranges (did not work for Logitech 930e with green light:
    #  Hue:         25-75
    #  Saturation:  95-255
    #  Value:       95-255
    # Experimental values with exposure=2 @ Home
    #  Hue:         40-80
    #  Saturation:  50-255
    #  Value:       70-255
    # Experimental values with exposure=1 @ Shop
    #  Hue:         40-90
    #  Saturation:  0-255
    #  Value:       95-255
    rrtarget_hue_low_limit = ntproperty('/SmartDashboard/vision/rrtarget/hue_low_limit', 40,
                                        doc='Hue low limit for thresholding (rrtarget mode)')
    rrtarget_hue_high_limit = ntproperty('/SmartDashboard/vision/rrtarget/hue_high_limit', 90,
                                         doc='Hue high limit for thresholding (rrtarget mode)')

    rrtarget_saturation_low_limit = ntproperty('/SmartDashboard/vision/rrtarget/saturation_low_limit', 0,
                                               doc='Saturation low limit for thresholding (rrtarget mode)')
    rrtarget_saturation_high_limit = ntproperty('/SmartDashboard/vision/rrtarget/saturation_high_limit', 255,
                                                doc='Saturation high limit for thresholding (rrtarget mode)')

    rrtarget_value_low_limit = ntproperty('/SmartDashboard/vision/rrtarget/value_low_limit', 95,
                                          doc='Value low limit for thresholding (rrtarget mode)')
    rrtarget_value_high_limit = ntproperty('/SmartDashboard/vision/rrtarget/value_high_limit', 255,
                                           doc='Value high limit for thresholding (rrtarget mode)')

    rrtarget_exposure = ntproperty('/SmartDashboard/vision/rrtarget/exposure', 0, doc='Camera exposure for rrtarget (0=auto)')

    def __init__(self, calib_file, test_mode=False):
        super().__init__(initial_mode='driver_pov', test_mode=test_mode)

        # Define cameras in system; uses 'by-id' reference to identifier camera by location on robot
        self.camera_device_front = '/dev/v4l/by-id/usb-046d_Logitech_Webcam_C930e_68EE436E-video-index0'    # Main driver POV and rrtarget processing
        self.camera_device_alt = '/dev/v4l/by-id/usb-046d_Logitech_Webcam_C930e_68EE436E-video-index0'      # Alternate driver POV

        self.add_cameras()

        self.generic_finder_front = GenericFinder("driver_pov", "front_camera", finder_id=1.0)
        self.add_target_finder(self.generic_finder_front) 

        self.generic_finder_alt = GenericFinder("driver_alt_pov", "alt_camera", finder_id=2.0)
        self.add_target_finder(self.generic_finder_alt)

        self.rrtarget_finder = RRTargetFinder2019(calib_file)       # Default finder_id=3.0
        self.add_target_finder(self.rrtarget_finder)

        #TODO make it a seperate finder to draw a line down the screen where the line at the bottom of the rocket will be

        # self.hatch_finder = HatchFinder2019(calib_file)
        # self.add_target_finder(self.hatch_finder)

        # self.line_finder = LineFinder2019(calib_file)
        # self.add_target_finder(self.line_finder)

        self.update_parameters()

        # start in rrtarget mode to get cameras going. Will switch to 'driver' after 1 sec.
        self.switch_mode('rrtarget')
        return

    def update_parameters(self):
        '''Update processing parameters from NetworkTables values.
        Only do this on startup or if "tuning" is on, for efficiency'''

        # Make sure to add any additional created properties which should be changeable

        self.rrtarget_finder.set_color_thresholds(self.rrtarget_hue_low_limit, self.rrtarget_hue_high_limit,
                                                  self.rrtarget_saturation_low_limit, self.rrtarget_saturation_high_limit,
                                                  self.rrtarget_value_low_limit, self.rrtarget_value_high_limit)
        return

    def add_cameras(self):
        '''add a single camera at /dev/videoN, N=camera_device'''

        self.add_camera('front_camera', self.camera_device_front, True)
        # Temporarily no second camera; uncomment when added
        #self.add_camera('alt_camera', self.camera_device_alt, False)
        return

    def mode_after_error(self):
    # Temporarily removed for one camera; replace isolated 'return' with code below
    #   if self.active_mode == 'driver_pov':
    #       return 'driver_alt_pov'
        return 'driver_pov'


# Main routine
if __name__ == '__main__':
    main(VisionServer2019)
