import sys
import cv2
from Draw import markWithCircle
from HarrisCorner import findCorners

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r,c = findCorners(gray, 11, 4)
m = markWithCircle(r,c,img)
cv2.imshow('f', m)
cv2.waitKey(0)