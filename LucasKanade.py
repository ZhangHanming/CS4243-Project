import numpy as np
import cv2
import sys


def trackFeatures(old_frame, new_frame, r, c):
    old_frame_pyramid = createPyramid(old_frame)
    new_frame_pyramid = createPyramid(new_frame)

    return computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r, c, 7)


def createPyramid(frame, minSize = 32, maxLevel = 5):
    pyramid = [frame]
    while(frame.shape[0] > minSize and frame.shape[1] > minSize and len(pyramid)<maxLevel):
        sample = downsample(frame)
        pyramid = [sample] + pyramid
        frame = sample

    return pyramid

# downsample by averabng a neighborhood of 4 pixels
def downsample(frame):
    new_frame = np.zeros(map(lambda x: x/2, frame.shape))
    for i in range(0,frame.shape[0],2):
        for j in range(0,frame.shape[1],2):
            new_frame[i/2][j/2] = frame[i:i+2,j:j+2].sum() / 4

    return new_frame

def computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r, c, ksize = 3):
    kernel = np.ones((ksize, ksize))
    resize = lambda x : x / 2 ** (len(old_frame_pyramid) - 1)
    r = map(resize, r)
    c = map(resize, c)


    # loop from the top of the pyramid
    for i in range(len(old_frame_pyramid)):        

        I = old_frame_pyramid[i]
        J = new_frame_pyramid[i]

        x, y = I.shape

        gx = np.zeros((x, y))
        gy = np.zeros((x, y))
        gx[:,0:y-1] = I[:,1:y] - I[:,0:y-1]
        gy[0:x-1,:] = I[1:x,:] - I[0:x-1,:]

        Ixx = gx * gx
        Ixy = gx * gy
        Iyy = gy * gy

        Wxx = cv2.filter2D(Ixx, -1, kernel)
        Wxy = cv2.filter2D(Ixy, -1, kernel)
        Wyy = cv2.filter2D(Iyy, -1, kernel)
        Gx = cv2.filter2D(gx*(I-J), -1, kernel)
        Gy = cv2.filter2D(gy*(I-J), -1, kernel)

        j = 0
        while(j < len(r)):
            # discard out of frame corners
            if(r[j] > x or c[j] > y):
                del r[j]
                del c[j]
                j = j-1
                continue

            try:
                Z = np.array([[Wxx[r[j]][c[j]], Wxy[r[j]][c[j]]], [Wxy[r[j]][c[j]], Wyy[r[j]][c[j]]]])
                b = np.array([[Gx[r[j]][c[j]]], [Gy[r[j]][c[j]]]])

                d = np.dot(np.linalg.inv(Z), b)

                r[j] += d[0,0]
                c[j] += d[1,0]
                r[j] = int(np.around(r[j]))
                c[j] = int(np.around(c[j]))
                
                if(i != len(old_frame_pyramid) - 1):
                    r[j] *= 2
                    c[j] *= 2
            except:
                print "Unexpected error:", sys.exc_info()[0]

            j = j + 1
    return r, c


