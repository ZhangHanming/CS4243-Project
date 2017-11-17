import numpy as np
import cv2
import math
from addImage import addImage

vPath = "Videos/sx.mp4"
imagePath = "Images/feather.jpg"
cols = np.loadtxt("cols.csv", delimiter=",")
rows = np.loadtxt("rows.csv", delimiter=",")

# Expecting format: cols[pointNumber,frameNumber]

corner_number = cols.shape[0]
cap = cv2.VideoCapture(vPath)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'IYUV')
out = cv2.VideoWriter('Videos/wing.avi', fourcc, fps, (width, height))

image = cv2.imread(imagePath, 1)
rotate_mat_size = int(image.shape[0] * 2)

# Read all frames and add image on each frame
while(1):
    ret, frame = cap.read()
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if(not ret or frame_number == int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        break

    # interate all corners' coordinates in one frame
    for i in range(0, corner_number):
        # r1: old row, r2: new row
        # c1: old col, c2: new col
        r1 = rows[i, frame_number-1]
        r2 = rows[i, frame_number]
        c1 = cols[i, frame_number-1]
        c2 = cols[i, frame_number]
        # Filter out the points in the body area, magic numbers are mearsured by hand
        if((c2 > 250 and c2 < 380) or (c1 > 250 and c2 < 380) or r1 > 340 or r2 > 340):
            continue
        distance = np.sqrt((r2 - r1)**2 + (c2 - c1)**2)
        # Only draw points thats moves, and ignore noise that moves rapidly
        if(distance > 1.5 and distance < 13):
            # give a random color for each feather (grey scale)
            random_grey_scale = np.random.uniform(0.5,1.0)
            new_image = (image * random_grey_scale).astype(np.uint8)
            angle = np.rad2deg(np.arctan2(c2 - c1, r2 - r1)) + 180
            # Make sure the feature is not so big
            scale = distance / 5.0
            new_rotate_mat_size = int(scale * rotate_mat_size)
            # Produce the new frame
            frame = addImage(r2, c2, angle, scale, new_rotate_mat_size, new_image, frame)
    out.write(frame)
cap.release()
out.release()
