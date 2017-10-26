import numpy as np
import cv2


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
    destHeight = dest.shape[0]
    destWidth = dest.shape[1]
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    imgROIx1 = 0
    imgROIx2 = imgHeight
    imgROIy1 = 0
    imgROIy2 = imgWidth
    x1 = pos[0] - imgHeight / 2
    x2 = pos[0] + imgHeight / 2
    y1 = pos[1] - imgWidth / 2
    y2 = pos[1] + imgWidth / 2
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
    img = img[imgROIx1:imgROIx2, imgROIy1:imgROIy2]
    b, g, r, a = cv2.split(img)
    overlayRBG = cv2.merge((b, g, r))
    mask = cv2.medianBlur(a, 3)
    roi = dest[x1:x2, y1:y2]
    destNew = cv2.bitwise_and(roi.copy(), roi.copy(),
                              mask=cv2.bitwise_not(mask))
    overlay = cv2.bitwise_and(overlayRBG, overlayRBG, mask=mask)
    dest[x1:x2, y1:y2] = cv2.add(destNew, overlay)
    return dest
