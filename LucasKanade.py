import numpy as np
import cv2

def trackFeatures(old_frame, new_frame, r, c):
    return None


def downsample(frame):
    new_frame = np.zeros(map(lambda x: x/2, frame.shape))
    for i in range(0,frame.shape[0],2):
        for j in range(0,frame.shape[1],2):
            new_frame[i/2][j/2] = frame[i:i+2,j:j+2].sum() / 4

    return new_frame
