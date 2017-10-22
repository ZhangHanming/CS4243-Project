import numpy as np
import cv2
from HarrisCorner import findCorners

cap = cv2.VideoCapture("Videos/traffic.mp4")


while(1):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    r, c = findCorners(frame_gray)
    for i in range(len(r)):
        frame = cv2.circle(frame, (c[i], r[i]), 5, (0, 0, 255), 1)

    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    break



cap.release()