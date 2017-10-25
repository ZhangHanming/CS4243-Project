import numpy as np
import cv2

def findCorners(frame, ksize = 13, kCorners = 200):
    x, y = frame.shape

    gx = np.zeros((x, y))
    gy = np.zeros((x, y))
    gx[:,0:y-1] = frame[:,1:y] - frame[:,0:y-1]
    gy[0:x-1,:] = frame[1:x,:] - frame[0:x-1,:]

    Ixx = gx * gx
    Ixy = gx * gy
    Iyy = gy * gy

    kernel = np.ones((ksize,ksize))
    Wxx = cv2.filter2D(Ixx, -1, kernel)
    Wxy = cv2.filter2D(Ixy, -1, kernel)
    Wyy = cv2.filter2D(Iyy, -1, kernel)

    eigMin = np.zeros(Wxx.shape)

    for i in range(eigMin.shape[0]):
        for j in range(eigMin.shape[1]):
            Wi = np.array([[Wxx[i][j], Wxy[i][j]], [Wxy[i][j], Wyy[i][j]]])
            D, V = np.linalg.eig(Wi)
            eigMin[i][j] = D.min()
    
    return selectCorners(eigMin, ksize, kCorners)


def selectCorners(eigMin, ksize, kCorners):
    c = []
    r = []
    rows = []
    cols = []
    for i in range(0,eigMin.shape[0]-ksize,13):
        for j in range(0,eigMin.shape[1]-ksize,13):
            m = eigMin[i:i+ksize, j:j+ksize]
            row = np.argmax(np.max(m, axis=0))+i
            col = np.argmax(np.max(m, axis=1))+j
            r.append(row)
            c.append(col)

    mins = []
    for i in range(len(r)):
        mins.append(eigMin[r[i]][c[i]])

    ind = np.argpartition(mins, -kCorners)[-kCorners:]
    for i in ind:
        rows.append(r[i])
        cols.append(c[i])

    return rows, cols




