import cv2
import numpy as np
import random
def nones(x):
    result = []
    for y in range(x):
        result.append(None)
    return result

class PiCamera:
    def __init__(self, camnum):
        # # Initialize a camera capture.
        # self.capture = cv2.VideoCapture(camnum)
        #
        # # Capture a few frames to get the camera used to the light.
        # for i in range(10):
        #     # @var ret - Returns whether or not the frame was read properly.
        #     # @var frame - The current frame.
        #     self.ret, self.frame = self.capture.read()
        self.TEST_IMGS = ['HC0_N.png','VC0_C.png','VL0_G.png', 'tape.jpg']

    def getCurrentFrame(self):
        # self.ret, self.frame = self.capture.read();
        self.frame = cv2.imread(random.choice(self.TEST_IMGS))
        return self.frame

    def getCurrentFrameResized(self, x, y):
        return cv2.resize(self.getCurrentFrame(), (x, y))

    def getCurrentFrameMultiplier(self, x, y):
        height, width, channels = self.getCurrentFrame().shape
        return cv2.resize(self.frame, (int(width * x), int(height * y)))

    def modifyThreshold(self, frame, value):
        ret, threshold = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), value, 255, cv2.THRESH_BINARY)
        return threshold

    def filterContours(self, countours, size):
        countours2 = np.empty(0)
        for countour in countours:
            if cv2.countourArea(countour) > size:
                countours2 = np.append(countour)
        return countours2

    def cleanUp(self):
    #    ser.close()
        capture.release()
        cv2.destroyAllWindows()

    def nw(self, name):
        #cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
