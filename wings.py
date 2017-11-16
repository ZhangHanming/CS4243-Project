import numpy as np
import cv2
import math
from addImage import addImage

vPath = "Videos/arm.mp4"
imagePath = "feather.jpg"
cols = np.loadtxt("cols.csv", delimiter=",")
rows = np.loadtxt("rows.csv", delimiter=",")

# cols[pointNumber][frameNumber]

corner_number = cols.shape[0]
threshold = 5.0

cap = cv2.VideoCapture(vPath)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'IYUV')
out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

image = cv2.imread(imagePath, 1)
rotate_mat_size = int(image.shape[1] * 2)
while(1):
    ret, frame = cap.read()
    if(not ret):
        break
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    for i in range(1, corner_number):
        r1 = rows[i - 1, frame_number]
        r2 = rows[i, frame_number]
        c1 = cols[i - 1, frame_number]
        c2 = cols[i, frame_number]
        if(r1 < 0 or r2 < 0 or c1 < 0 or c2 < 0):
            continue
        distance = np.sqrt((r2 - r1)**2 + (c2 - c1)**2)
        if(distance > 2.5 and distance < 15):
            random_grey_scale = np.random.uniform(0.5,1.0)
            new_image = (image * random_grey_scale).astype(np.uint8)
            angle = np.rad2deg(np.arctan2(c2 - c1, r2 - r1)) + 180
            scale = distance / threshold
            new_rotate_mat_size = int(scale * 300)
            frame = addImage(r2, c2, angle, scale, new_rotate_mat_size, new_image, frame)
    out.write(frame)
cap.release()
out.release()
