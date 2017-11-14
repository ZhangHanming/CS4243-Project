import numpy as np
import cv2
import math
from addImage import addImage

vPath = "Videos/mouse.mp4"
imagePath = "feather.png"
cols = np.loadtxt("cols.csv", delimiter=",")
rows = np.loadtxt("rows.csv", delimiter=",")

# cols[pointNumber][frameNumber]

# Calculate the displacement of each corner in all frames
row_displace = rows[:, 1:-1] - rows[:, 0:-2]
col_displace = cols[:, 1:-1] - cols[:, 0:-2]

corner_number = cols.shape[0]
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
rotate_mat_size = int(image.shape[1] * 2)
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
