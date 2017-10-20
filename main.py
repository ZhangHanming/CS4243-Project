import numpy as np
import cv2

cap = cv2.VideoCapture("Videos/traffic.mp4")

while(True):
    ret, frame = cap.read()

    if(not ret):
        break

    print frame.shape
