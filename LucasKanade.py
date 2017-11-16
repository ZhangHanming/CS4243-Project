import numpy as np
import cv2
import sys


def trackFeatures(old_frame, new_frame, r, c):
    old_frame_pyramid = createPyramid(old_frame)
    new_frame_pyramid = createPyramid(new_frame)

    return computeOpticalFlow(old_frame_pyramid, new_frame_pyramid, r, c, 17)


def createPyramid(frame, minSize = 64, maxLevel = 5):
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
    gaussian1D = cv2.getGaussianKernel(ksize, 1)
    kernel = np.dot(gaussian1D, np.transpose(gaussian1D))

    scaledR = scaleVector(r, len(old_frame_pyramid))
    scaledC = scaleVector(c, len(old_frame_pyramid))

    upsample = lambda x : x * 2
    d = [np.array([[0.],[0.]])]*len(r)



    # loop from the top of the pyramid
    for i in range(len(old_frame_pyramid)):        
        d = map(upsample, d)

        I = old_frame_pyramid[i].astype(float)
        J = new_frame_pyramid[i].astype(float)

        # Smoothen to remove noise but lose sharpness
        I = cv2.GaussianBlur(I, (3,3), 1)
        J = cv2.GaussianBlur(J, (3,3), 1)

        x, y = I.shape
        gx = np.zeros((x, y))
        gy = np.zeros((x, y))
        gx[:, 0:y - 1] = I[:, 1:y] - I[:, 0:y - 1]
        gy[0:x - 1, :] = I[1:x, :] - I[0:x - 1, :]


        Ixx = gx * gx
        Ixy = gx * gy
        Iyy = gy * gy

        j = 0
        counter = 0

        while(j < len(scaledR[0])):        
            try:
                row = scaledR[i][j]
                col = scaledC[i][j]

                
                halfKSize = int(ksize / 2)
                dint = np.around(d).astype(int)
                Jrow = row + dint[j][1,0]
                Jcol = col + dint[j][0,0]
                gt = I[row-halfKSize:row+halfKSize+1,col-halfKSize:col+halfKSize+1] - J[Jrow-halfKSize:Jrow+halfKSize+1,Jcol-halfKSize:Jcol+halfKSize+1]

                gtgx = (gt*gx[row-halfKSize:row+halfKSize+1,col-halfKSize:col+halfKSize+1]).sum()
                gtgy = (gt*gy[row-halfKSize:row+halfKSize+1,col-halfKSize:col+halfKSize+1]).sum()
                gxgx = (Ixx[row-halfKSize:row+halfKSize+1,col-halfKSize:col+halfKSize+1]).sum()
                gxgy = (Ixy[row-halfKSize:row+halfKSize+1,col-halfKSize:col+halfKSize+1]).sum()
                gygy = (Iyy[row-halfKSize:row+halfKSize+1,col-halfKSize:col+halfKSize+1]).sum()

                Z = np.array([[gxgx, gxgy], [gxgy, gygy]])
                b = np.array([[gtgx], [gtgy]])
                    
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


