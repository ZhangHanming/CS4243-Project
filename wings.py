import numpy as np
import cv2
import math

vPath = "Videos/mouse.mp4"
imagePath = ""
cols = np.loadtxt("cols.csv", delimiter=",")
rows = np.loadtxt("rows.csv", delimiter=",")

# cols[pointNumber][frameNumber]

# Calculate the displacement of each corner in all frames
row_displace = rows[:, 1:-1] - rows[:, 0:-2]
col_displace = cols[:, 1:-1] - cols[:, 0:-2]

corner_number = cols.shape(0)
threshold = 2
distance_list = np.sqrt(row_displace**2 + col_displace**2)
scale_list = np.divide(distance_list, np.mean(
    distance_list[distance_list > 0]))

# Angles of the corners' movement
angle_list = np.zeros(distance_list.shape)
angle_list[distance_list > threshold] = np.rad2deg(np.arctan2(
    row_displace[distance_list > threshold], col_displace[distance_list > threshold]))


cap = cv2.VideoCapture(vPath)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'IYUV')
out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

image = cv2.imread(imagePath, -1)
rotate_mat_size = int(image.shape(1) * 2)
while(1):
    ret, frame = cap.read()
    if(not ret):
        break
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    for i in range(corner_number):
        if(distance_list[i, frame_number - 1] <= threshold):
            continue
        col = int(cols[i, frame_number])
        row = int(rows[i, frame_number])
        angle = angle_list[i, frame_number - 1]
        scale = scale_list[frame_number - 1]
        new_rotate_mat_size = int(scale * rotate_mat_size)
        new_frame = addImage(row, col, angle, scale,
                             new_rotate_mat_size, image, frame)
        out.write(new_frame)
cap.release()
out.release()


def addImage(row, col, angle, scale, size, img, bg):
    img_width = image.shape(0)
    img_height = image.shape(1)
    bg_width = bg.shape(0)
    bg_height = bg.shape(1)
    M = cv2.getRotationMatrix2D((img_width / 2, 0), angle, scale)
    rotated_img = cv2.warpAffine(image, M, (size, size))
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
    ret, mask = cv2.threshold(img2Gray, 5, 255, cv2.THRESH_BINARY)
    img_ROI = cv2.bitwise_and(img_ROI, img_ROI, mask=mask)
    bg_ROI = bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2]
    bg[bg_ROI_row1:bg_ROI_row2, bg_ROI_col1:bg_ROI_col2] = cv2.add(
        bg_ROI, img_ROI)
    return bg
