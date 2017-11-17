import numpy as np
import cv2


def addImage(row, col, angle, scale, size, img, bg):
    """Funtion to paste an image onto a background image
    Args:
        row: the row number of center to be pasted on the background
        col: the col number of center to be pasted on the background
        angle: the anti-clockwise angle of the image (in degree)
        scale: the resizing scale of the image
        img: image to be pasted
        bg: backgroung image

    Returns:
        bg: finshed image

    """
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
    # Set the region of interest for image and background
    img_ROI_row1 = 0
    img_ROI_row2 = size
    img_ROI_col1 = 0
    img_ROI_col2 = size
    bg_ROI_row1 = row - half_size
    bg_ROI_row2 = bg_ROI_row1 + size
    bg_ROI_col1 = col - half_size
    bg_ROI_col2 = bg_ROI_col1 + size

    # Handle exceeding boundary cases
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

    # Create a mask to cut the black part of the image
    ret, mask = cv2.threshold(img2Gray, 60, 255, cv2.THRESH_BINARY)
    # Create a mask to clean the roi on the background
    mask_inv = cv2.bitwise_not(mask)

    # Paste images by cv2.add
    img_ROI = cv2.bitwise_and(img_ROI, img_ROI, mask=mask)
    bg_ROI = bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2]
    bg_ROI = cv2.bitwise_and(bg_ROI, bg_ROI, mask = mask_inv)
    overlay = cv2.add(bg_ROI, img_ROI)
    bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2] = overlay

    return bg
