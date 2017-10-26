import numpy as np
import cv2


def findCorners(frame, ksize=13, kCorners=200):
    x, y = frame.shape

    #gx, gy = np.gradient(frame)

    # gx = np.zeros((x, y))
    # gy = np.zeros((x, y))
    # gx[:, 0:y - 1] = frame[:, 1:y] - frame[:, 0:y - 1]
    # gy[0:x - 1, :] = frame[1:x, :] - frame[0:x - 1, :]

    gx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize = ksize)
    gy = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize = ksize)

    Ixx = gx * gx
    Ixy = gx * gy
    Iyy = gy * gy

    #kernel = np.ones((ksize,ksize))
    kernel = getGaussKernels(ksize)
    Wxx = cv2.filter2D(Ixx, -1, kernel)
    Wxy = cv2.filter2D(Ixy, -1, kernel)
    Wyy = cv2.filter2D(Iyy, -1, kernel)

    response = np.zeros(Wxx.shape)

    for i in range(response.shape[0]):
        for j in range(response.shape[1]):
            Wi = np.array([[Wxx[i][j], Wxy[i][j]], [Wxy[i][j], Wyy[i][j]]])
            # D, V = np.linalg.eig(Wi)
            response[i][j] = np.linalg.det(Wi)-0.04*np.trace(Wi)**2

    return selectCorners(response, ksize, kCorners)


def selectCorners(response, ksize, kCorners):
    c = []
    r = []
    rows = []
    cols = []
    for i in range(0, response.shape[0] - ksize, ksize):
        for j in range(0, response.shape[1] - ksize, ksize):
            m = response[i:i + ksize, j:j + ksize]
            index = np.argmax(m)
            row = int(index / ksize) + i
            col = int(index % ksize) + j
            r.append(row)
            c.append(col)

    localmax = []
    for i in range(len(r)):
        localmax.append(response[r[i]][c[i]])

    ind = np.argpartition(localmax, -kCorners)[-kCorners:]
    for i in ind:
        rows.append(r[i])
        cols.append(c[i])

    return rows, cols


def getGaussKernels(k, sigma=1.0):
    # Generate a Gkernel with length k and sigma
    ax = np.arange(-k // 2 + 1.0, k // 2 + 1.0)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
    return kernel / np.sum(kernel)
