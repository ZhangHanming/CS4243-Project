import numpy as np
import cv2


def addEffect(cornorPos, videoCap):
    rainbow = cv2.imread("rainbow.png")
    width = cv2.VideoCapture.get(CV_CAP_PROP_FRAME_WIDTH)
    height = cv2.VideoCapture.get(CV_CAP_PROP_FRAME_HEIGHT)
    empty = np.zeros(height, width, 4)
    while(1):
        ret, frame = videoCap.read()
        if(not ret):
            break
        emptyNew = empty
