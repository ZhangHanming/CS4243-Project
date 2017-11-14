import numpy as np
import cv2
import math


def addEffect(videoPath, imagePath, rows, cols):
    cap = cv2.VideoCapture(videoPath)
    rainbow = cv2.imread(imagePath, -1)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'IYUV')
    out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))
    while(1):
        ret, frame = cap.read()
        if(not ret):
            break
        frameNumber = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        corner = np.array([int(cols[frameNumber]), int(rows[frameNumber])])
        frame = pasteImage(rainbow, frame, corner)
        out.write(frame)
    cap.release()
    out.release()


def pasteImage(img, dest, pos):
    """
    @brief paste a image onto the background image
    @param img The image to be pasted
    @param dest The background image
    @pos coordinate of background to be pasted, align to the center of the source image
    @return the result image
    """
    destHeight = int(dest.shape[0])
    destWidth = int(dest.shape[1])
    degree = math.degrees(
        math.atan((destWidth / 2 - pos[0]) / (destHeight - pos[1])))
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    imgDiagonal = int(math.sqrt(imgHeight**2 + imgWidth**2)) - 1
    M = cv2.getRotationMatrix2D((imgWidth / 2, imgHeight / 2), degree, 1)
    # Change the center of rotation matrix from cv2
    M[0, 2] += int(imgDiagonal / 2 - imgWidth / 2)
    M[1, 2] += int(imgDiagonal / 2 - imgHeight / 2)
    rotatedImg = cv2.warpAffine(img, M, (imgDiagonal, imgDiagonal))
    # Change the size of image to larget size
    imgROIx1 = 0
    imgROIx2 = imgDiagonal
    imgROIy1 = 0
    imgROIy2 = imgDiagonal
    # Positions on the background to be pasted
    if(imgDiagonal % 2 == 0):
        alpha = 1
    else:
        alpha = 0

    x1 = int(pos[0] - imgDiagonal / 2 + alpha)
    x2 = int(pos[0] + imgDiagonal / 2)
    y1 = int(pos[1] - imgDiagonal / 2 + alpha)
    y2 = int(pos[1] + imgDiagonal / 2)
    # Handle corner cases
    if(x1 < 0):
        imgROIx1 = -x1
        x1 = 0
    if(x2 > destHeight):
        imgROIx2 = int(imgHeight - x2 + destHeight)
        x2 = destHeight
    if(y1 < 0):
        imgROIy1 = -y1
        y1 = 0
    if(y2 > destWidth):
        imgROIy2 = int(imgWidth - y2 + destWidth)
        y2 = destWidth
    rotatedImg = rotatedImg[imgROIx1:imgROIx2, imgROIy1:imgROIy2]
    b, g, r, a = cv2.split(rotatedImg)
    overlayRBG = cv2.merge((b, g, r))
    img2Gray = cv2.cvtColor(overlayRBG, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2Gray, 5, 255, cv2.THRESH_BINARY)
    maskInv = cv2.bitwise_not(mask)
    maskAlpha = cv2.bitwise_not(a)
    roi = dest[x1:x2 + 1, y1:y2 + 1]
    print roi.shape
    print maskAlpha.shape
    destNew = cv2.bitwise_and(roi.copy(), roi.copy(), mask=maskAlpha)
    overlay = cv2.bitwise_and(overlayRBG, overlayRBG, mask=mask)
    dest[x1:x2 + 1, y1:y2 + 1] = cv2.add(destNew, overlay)
    return dest
