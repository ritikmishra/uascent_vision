import Utils
import cv2

import cv2
import numpy as np
from Utils import PiCamera
import detect
from networktables import NetworkTables
from Utils import nones
import time

# define our boundary for red in BGR
# THE COLORS ARE IN [BLUE, GREEN, RED]
# DO NOT FORGET!
boundary = [
    ([120, 133, 0],[255, 255, 255])
]

lower = np.array(boundary[0][0], dtype="uint8")
upper = np.array(boundary[0][1], dtype="uint8")

cam = PiCamera(0)
##### How many cameras are we looking a
camnum = 1
#####
#for x in range(camnum):
#    cams.append(PiCamera(x))


# Initalize variables
frames = np.zeros(720, 480)
frame_mask = frames

# Connect to RoboRIO via networktable
NetworkTables.initialize(server='roborio-2502-frc.local')
visionTable = NetworkTables.getTable('PiVision')

oldtime = time.time() * 1000
sequence = 0
starttime = oldtime

while True:
    # open eyes
    frames[x] = cam.getCurrentFrameResized(720, 480)

    # ignore irrelevant colors
    frame_mask[camnum] = cv2.inRange(frame, lower, upper)

    offset = detect.track_range(frame_mask[camnum])

    print(offset[0])
    cv2.imshow(str(camnum), frames[camnum])

    currenttime = time.time() * 100
    visionTable.putNumber("offset", float(offset[0]))
    visionTable.putNumber("sequence", float(sequence))
    visionTable.putNumber("time", float(currenttime - starttime))
    visionTable.putNumber("timeelapsed", float(currenttime - oldtime))
    oldtime = currenttime

    sequence += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Utils.cleanUp()
