import numpy as np
import cv2
import sys


def trackFeatures(old_frame, new_frame, r, c):
    old_frame_pyramid = createPyramid(old_frame)
    new_frame_pyramid = createPyramid(new_frame)

    return computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r, c, 17)


def createPyramid(frame, minSize = 16, maxLevel = 5):
    frame = frame.astype(float)
    pyramid = [frame]
    while(frame.shape[0] > minSize and frame.shape[1] > minSize and len(pyramid)<maxLevel):
        sample = gaussianSubsample(frame)
        pyramid = [sample] + pyramid
        frame = sample

    return pyramid

def scaleVector(v, length):
    result = [v]
    downsample = lambda x : x / 2
    for i in range(length - 1):
        scaled = map(downsample, v)
        result = [scaled] + result
        v = scaled

    return result

def gaussianSubsample(frame):
    gaussian1D = cv2.getGaussianKernel(5, 1)
    kernel = np.dot(gaussian1D, np.transpose(gaussian1D))

    frame = cv2.filter2D(frame, -1, kernel)
    new_frame = np.zeros(map(lambda x: x/2, frame.shape))
    new_frame[:,:] = frame[0:frame.shape[0]-1:2, 0:frame.shape[1]-1:2]
    return new_frame

def computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r, c, ksize = 17):
    # kernel = np.ones((ksize, ksize))
    gaussian1D = cv2.getGaussianKernel(ksize, 1) * ksize
    kernel = np.dot(gaussian1D, np.transpose(gaussian1D))

    scaledR = scaleVector(r, len(old_frame_pyramid))
    scaledC = scaleVector(c, len(old_frame_pyramid))

    upsample = lambda x : x * 2
    d = [np.array([[0.],[0.]])]*len(r)



    # loop from the top of the pyramid
    for i in range(len(old_frame_pyramid)):        
        d = map(upsample, d)

        I = old_frame_pyramid[i]
        J = new_frame_pyramid[i]

        I = cv2.GaussianBlur(I, (3,3), 0)
        J = cv2.GaussianBlur(J, (3,3), 0)

        x, y = I.shape
        
        # gx = cv2.Sobel(I, cv2.CV_64F, 1, 0, ksize = 1) 
        # gy = cv2.Sobel(I, cv2.CV_64F, 0, 1, ksize = 1) 



        # gx = np.zeros((x, y))
        # gy = np.zeros((x, y))
        # gx[:, :-1] = I[:, 1:] - I[:, :-1]
        # gy[:-1, :] = I[1:, :] - I[:-1, :]

        gx = cv2.filter2D(I, cv2.CV_64F, 0.25 * np.array([[-1,1],[-1,1]]))
        gy = cv2.filter2D(I, cv2.CV_64F, 0.25 * np.array([[-1,-1],[1,1]]))

        Ixx = gx * gx
        Ixy = gx * gy
        Iyy = gy * gy

        Wxx = cv2.filter2D(Ixx, cv2.CV_64F, kernel)
        Wxy = cv2.filter2D(Ixy, cv2.CV_64F, kernel)
        Wyy = cv2.filter2D(Iyy, cv2.CV_64F, kernel)

        j = 0
        counter = 0

        while(j < len(scaledR[0])):        
            try:
                row = scaledR[i][j]
                col = scaledC[i][j]

                translateM = np.float32([[1,0,-d[j][0,0]],[0,1,-d[j][1,0]]])
                
                # translateM = np.float32([[1,0,0.],[0,1,0.]])
                translatedJ = cv2.warpAffine(J, translateM, (J.shape[1], J.shape[0]))

                gt = cv2.filter2D(I, cv2.CV_64F, 0.25 * np.ones((2,2))) + cv2.filter2D(translatedJ, cv2.CV_64F, -0.25 * np.ones((2,2)))
                # gt = I - translatedJ


                Gx = cv2.filter2D(gt*gx, cv2.CV_64F, kernel)
                Gy = cv2.filter2D(gt*gy, cv2.CV_64F, kernel)

                Z = np.array([[Wxx[row,col], Wxy[row,col]], [Wxy[row,col], Wyy[row,col]]])
                b = np.array([[Gx[row,col]], [Gy[row,col]]])
                    
                movement = np.dot(np.linalg.inv(Z), b)         
                
                d[j] = d[j] + movement

                if(np.linalg.norm(movement) == 0 or counter >= 10):
                    j += 1
                    counter = 0
                else:
                    counter += 1

            except Exception as e:
                j += 1

    d = np.around(d)

    c = np.add(c, map(lambda x : int(x[0,0]), d))
    r = np.add(r, map(lambda x : int(x[1,0]), d))

    return r.tolist(), c.tolist()


