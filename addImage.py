import numpy as np
import cv2


def addImage(row, col, angle, scale, size, img, bg):
    row = int(row)
    col = int(col)
    img_width = img.shape[1]
    img_height = img.shape[0]
    bg_width = bg.shape[1]
    bg_height = bg.shape[0]
    M = cv2.getRotationMatrix2D((img_width / 2, 0), angle, scale)
    # Change the center of rotation matrix from cv2
    M[0, 2] += int(scale * img_height) - int(img_width / 2)
    M[1, 2] += int(scale * img_height)
    rotated_img = cv2.warpAffine(img, M, (size, size))
    half_size = size / 2
    img_ROI_row1 = 0
    img_ROI_row2 = size
    img_ROI_col1 = 0
    img_ROI_col2 = size
    bg_ROI_row1 = row - half_size
    bg_ROI_row2 = bg_ROI_row1 + size
    bg_ROI_col1 = col - half_size
    bg_ROI_col2 = bg_ROI_col1 + size

    # Handle exceed boundary cases
    if(bg_ROI_row1 < 0):
        img_ROI_row1 = -bg_ROI_row1
        bg_ROI_row1 = 0
        bg_ROI_row2 = img_ROI_row2 - img_ROI_row1

    if(bg_ROI_row2 > bg_height):
        img_ROI_row2 = size - (bg_ROI_row2 - bg_height)
        bg_ROI_row2 = bg_ROI_row1 + img_ROI_row2 - img_ROI_row1

    if(bg_ROI_col1 < 0):
        img_ROI_col1 = -bg_ROI_col1
        bg_ROI_col1 = 0
        bg_ROI_col2 = img_ROI_col2 - img_ROI_col1

    if(bg_ROI_col2 > bg_width):
        img_ROI_col2 = size - (bg_ROI_col2 - bg_width)
        bg_ROI_col2 = bg_ROI_col1 + img_ROI_col2 - img_ROI_col1

    img_ROI = rotated_img[img_ROI_row1:img_ROI_row2, img_ROI_col1:img_ROI_col2]
    img2Gray = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2Gray, 50, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img_ROI = cv2.bitwise_and(img_ROI, img_ROI, mask=mask)
    bg_ROI = bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2]
    bg_ROI = cv2.bitwise_and(bg_ROI, bg_ROI, mask = mask_inv)
    #print "___________________"
    #print "size", size
    #print "pos r c", row,col
    #print "img row", img_ROI_row1,img_ROI_row2
    #print "img col", img_ROI_col1,img_ROI_col2
    #print "bg row", bg_ROI_row1,bg_ROI_row2
    #print "bg col", bg_ROI_col1,bg_ROI_col2
    #print "bg", bg_ROI.shape
    #print "img", img_ROI.shape
    overlay = cv2.add(bg_ROI, img_ROI)
    bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2] = overlay
    #print bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2].shape
    return bg
