import numpy as np
import cv2


def addImage(row, col, angle, scale, size, img, bg):
    img_width = img.shape[0]
    img_height = img.shape[1]
    bg_width = bg.shape[0]
    bg_height = bg.shape[1]
    M = cv2.getRotationMatrix2D((img_width / 2, 0), angle, scale)
    rotated_img = cv2.warpAffine(img, M, (size, size))
    half_size = size / 2
    img_ROI_row1 = 0
    img_ROI_row2 = size
    img_ROI_col1 = 0
    img_ROI_col2 = size
    bg_ROI_row1 = int(row - half_size)
    bg_ROI_row2 = int(row + half_size)
    bg_ROI_col1 = int(col - half_size)
    bg_ROI_col2 = int(col + half_size)

    # Handle exceed boundary cases
    if(bg_ROI_row1 < 0):
        img_ROI_row1 = -bg_ROI_row1
        bg_ROI_row1 = 0
    if(bg_ROI_row2 > bg_height):
        img_ROI_row2 = size - bg_ROI_row2 + bg_height
        bg_ROI_row2 = bg_height
    if(bg_ROI_col1 < 0):
        img_ROI_col1 = -img_ROI_col1
        bg_ROI_col1 = 0
    if(bg_ROI_col2 > bg_width):
        img_ROI_col2 = size - bg_ROI_col2 + bg_width
        bg_ROI_col2 = bg_width

    # ensure the size is same
    if(img_ROI_col2 - img_ROI_col1 != bg_ROI_col2 - bg_ROI_col1):
        bg_ROI_col2 = bg_ROI_col1 + img_ROI_col2 - img_ROI_col1
    if(img_ROI_row2 - img_ROI_row1 != bg_ROI_row2 - bg_ROI_row1):
        bg_ROI_row2 = bg_ROI_row1 + img_ROI_col2 - img_ROI_col1

    img_ROI = rotated_img[img_ROI_row1:img_ROI_row2, img_ROI_col1:img_ROI_col2]
    img2Gray = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2Gray, 0, 255, cv2.THRESH_BINARY)
    img_ROI = cv2.bitwise_and(img_ROI, img_ROI, mask=mask)
    bg_ROI = bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2]
    bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2] = cv2.add(
        bg_ROI, img_ROI)
    return bg
