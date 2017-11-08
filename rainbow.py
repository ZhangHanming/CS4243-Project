import numpy as np
import cv2
import math


def addEffect(cornerPos, videoPath, imagePath):
    cap = cv2.VideoCapture(videoPath)
    rainbow = cv2.imread(imagePath)
    width = cv2.VideoCapture.get(CV_CAP_PROP_FRAME_WIDTH)
    height = cv2.VideoCapture.get(CV_CAP_PROP_FRAME_HEIGHT)
    fps = cv2.VideoCapture.get(CV_CAP_PROP_FPS)
    out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))
    while(1):
        ret, frame = videoCap.read()
        if(not ret):
            break
        frameNumber = cv2.VideoCapture.get(CV_CAP_PROP_FRAME_FRAMES)
        frame = pasteImage(rainbow, frame, cornerPos[frameNumber])
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
    destHeight = float(dest.shape[0])
    destWidth = float(dest.shape[1])
    degree = math.degrees(
        math.atan((destWidth / 2 - pos[0]) / (destHeight - pos[1])))
    print degree
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    imgDiagonal = int(math.sqrt(imgHeight**2 + imgWidth**2)) - 1
    M = cv2.getRotationMatrix2D((imgWidth / 2, imgHeight / 2), degree, 1)
    # Change the center of rotation matrix from cv2
    M[0, 2] += int(imgDiagonal / 2 - imgWidth / 2)
    M[1, 2] += int(imgDiagonal / 2 - imgHeight / 2)
    rotatedImg = cv2.warpAffine(img, M, (imgDiagonal, imgDiagonal))
    imgROIx1 = 0
    imgROIx2 = imgDiagonal
    imgROIy1 = 0
    imgROIy2 = imgDiagonal
    x1 = pos[0] - imgDiagonal / 2
    x2 = pos[0] + imgDiagonal / 2
    y1 = pos[1] - imgDiagonal / 2
    y2 = pos[1] + imgDiagonal / 2
    # Handle corner cases
    if(x1 < 0):
        imgROIx1 = -x1
        x1 = 0
    if(x2 > destHeight):
        imgROIx2 = imgHeight - x2 + destHeight
        x2 = destHeight
    if(y1 < 0):
        imgROIy1 = -y1
        y1 = 0
    if(y2 > destWidth):
        imgROIy2 = imgWidth - y2 + destWidth
        y2 = destWidth
    rotatedImg = rotatedImg[imgROIx1:imgROIx2, imgROIy1:imgROIy2]
    b, g, r, a = cv2.split(rotatedImg)
    overlayRBG = cv2.merge((b, g, r))
    img2Gray = cv2.cvtColor(overlayRBG, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2Gray, 0, 255, cv2.THRESH_BINARY)
    maskInv = cv2.bitwise_not(mask)
    maskAlpha = cv2.medianBlur(a, 3)
    roi = dest[x1:x2, y1:y2]
    print rotatedImg.shape
    print roi.shape
    print maskInv.shape
    destNew = cv2.bitwise_and(roi.copy(), roi.copy(), mask=maskInv)
    overlay = cv2.bitwise_and(overlayRBG, overlayRBG, mask=mask)
    dest[x1:x2, y1:y2] = cv2.add(destNew, overlay)
    return dest
