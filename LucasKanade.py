import numpy as np
import cv2
import sys


def trackFeatures(old_frame, new_frame, r, c):
    old_frame_pyramid = createPyramid(old_frame)
    new_frame_pyramid = createPyramid(new_frame)

    return computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r, c, 15)


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
    resizeToMinLevel = lambda x : x / 2 ** (len(old_frame_pyramid) - 1)
    r = map(resizeToMinLevel, r)
    c = map(resizeToMinLevel, c)

    upsample = lambda x : x * 2
    d = [np.array([[0.],[0.]])]*len(r)

    # loop from the top of the pyramid
    for i in range(len(old_frame_pyramid)):        
        d = map(upsample, d)
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

        j = 0
        while(j < len(r)):
            # discard out of frame corners
            if(r[j] > x or c[j] > y):
                del r[j]
                del c[j]
                del d[j]
                continue

        
            try:
                row = r[j]
                col = c[j]

                translateM = np.float32([[1,0,-d[j][0,0]],[0,1,-d[j][1,0]]])
                translatedJ = cv2.warpAffine(J, translateM, (J.shape[1], J.shape[0]))

                Gx = cv2.filter2D((I-translatedJ)*gx, -1, kernel)
                Gy = cv2.filter2D((I-translatedJ)*gy, -1, kernel)

                Z = np.array([[Wxx[row][col], Wxy[row][col]], [Wxy[row][col], Wyy[row][col]]])
                b = np.array([[Gx[row][col]], [Gy[row][col]]])

                d[j] += np.dot(np.linalg.inv(Z), b)
                
                if(i != len(old_frame_pyramid) - 1):
                    r[j] *= 2
                    c[j] *= 2
            except Exception as e:
                print(e)

            j = j + 1

    r = np.add(r, map(lambda x : int(x[0,0]), d))
    c = np.add(c, map(lambda x : int(x[1,0]), d))
    return r, c


