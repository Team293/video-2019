# VisionServer

This is the Python vision server ported from LigerBots (Team 2877).  It's intended to run on a coprocessor (e.g., Raspberry Pi 3 B+) on the robot.

The server can be "controlled" through NetworkTables. The NT variables are all under /SmartDashboard/vision.

Vision Server Control NT variables:
* /SmartDashboard/vision/active_mode = current vision processing mode (to retrieve the value from NT, use 'vision/active_mode')
  This is a string, with specific values.
  - "driver_pov" = Front-facing camera for primary driving POV only
  - "driver_alt_pov" = Optional alternate POV camera for driving only; software modifications required to activate.
  - "rrtarget" = Front-facing camera in retroreflective target acquition mode.

* /SmartDashboard/vision/tuning = Tuning mode; default False. Reads processing parameters each time (see Indicators notes below)

* /SmartDashboard/vision/write_images = Turn on saving of images; default False (see Indicators notes below)
  
Vision Server Target Information NT variable:
* /SmartDashboard/vision/target_info  = results of the target search. (to retrieve the array from NT, use 'vision/target_info')
  All values are floats, because NT arrays need to be a uniform type. Values are:
  * target_info[0] = timestamp of image in seconds.
  * target_info[1] = success (1.0) OR failure (0.0)
  * target_info[2] = mode (1='driver_pov', 2='driver_alt_pov', 3='rrtarget')
  * target_info[3] = distance to target (inches)
  * target_info[4] = angle1 to target (radians) -- angle displacement of robot to target
  * target_info[5] = angle2 of target (radians) -- angle displacement of target to robot

Vision Server Configurations NT variables (defaults for nominal operation):
* /SmartDashboard/vision/rrtarget/hue_low_limit = Hue low limit for thresholding for rrtarget mode; default 40
* /SmartDashboard/vision/rrtarget/hue_high_limit = Hue high limit for thresholding for rrtarget mode; default 90
* /SmartDashboard/vision/rrtarget/saturation_low_limit = Saturation low limit for thresholding for rrtarget mode; default 0
* /SmartDashboard/vision/rrtarget/saturation_high_limit = Saturation high limit for thresholding for rrtarget mode; default 255
* /SmartDashboard/vision/rrtarget/value_low_limit = Value low limit for thresholding for rrtarget mode; default 95
* /SmartDashboard/vision/rrtarget/value_high_limit = Value high limit for thresholding for rrtarget mode; default 255
* /SmartDashboard/vision/output_fps_limit = FPS limit of frames sent to MJPEG server; default 1000, large number for no limit
* /SmartDashboard/vision/output_port = TCP port for main image output; default 1190

Vision Server Static Configuration NT variables (set in software):
* /SmartDashboard/vision/width = Image width; default 424
* /SmartDashboard/vision/height = Image height; default 240
* /SmartDashboard/vision/fps = FPS from camera; default 30


Indicators (will only be present on the final stream, 1190):
* Test Mode (text): The VIsion Server is in test mode and set up a local set of NT. WARNING: The Vision Server will not commmunicate its NT with the Roborio's NT, since they are completely different tables. To change the mode, go into the Raspberry Pi and change start_server so that args includes/not include the tag '--test'
* Recording images (red dot): When the NT variable 'write_images' is turned on, images will be saved every 1/2 second to the directory saved_images under the server directory. The Raspberry Pi must have read-write file system enabled.
* Tuning On (text): When the NT variable 'tuning' is turned on, the server's NT variables will communicate with the individual finders' attributes such as HSV values. However, only tuning for HSV values is currently set up.
