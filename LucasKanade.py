import numpy as np
import cv2

def trackFeatures(old_frame, new_frame, r, c):
    old_frame_pyramid = createPyramid(old_frame)
    new_frame_pyramid = createPyramid(new_frame)

    # loop over each corner
    for i in range(len(r)):
        r[i], c[i] = computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r[i], c[i])

    return r, c


def createPyramid(frame, minSize = 32):
    pyramid = [frame]
    while(frame.shape[0] > minSize and frame.shape[1] > minSize):
        sample = downsample(frame)
        pyramid = [sample] + pyramid
        frame = sample

    return pyramid



def downsample(frame):
    new_frame = np.zeros(map(lambda x: x/2, frame.shape))
    for i in range(0,frame.shape[0],2):
        for j in range(0,frame.shape[1],2):
            new_frame[i/2][j/2] = frame[i:i+2,j:j+2].sum() / 4

    return new_frame

def computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r, c):
    #TODO
    return


