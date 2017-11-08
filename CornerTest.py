import sys
import cv2
from Draw import markWithCircle
from HarrisCorner import findCorners

# Video Reader
cap = cv2.VideoCapture("Videos/test2.mp4")
ret, old_frame = cap.read()
old_frame_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
r, c = findCorners(old_frame_gray, 11, 4)
m = markWithCircle(r, c, old_frame)
cv2.imshow('f', m)
cv2.waitKey(0)
