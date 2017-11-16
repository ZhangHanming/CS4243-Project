import cv2
import numpy as np
from LucasKanade import computeOpticalFlow
from HarrisCorner import findCorners
from Draw import markWithCircle
from LucasKanade import trackFeatures

img = cv2.imread('Images/checkboard.png')
old_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)

r, c = findCorners(old_gray, kCorners=50)

new_img = cv2.imread('Images/new.png')
new_gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY).astype(float)



# cv2.imshow('f', markWithCircle(r, c, old_gray))
# cv2.waitKey(0)

# new_r, new_c = computeOpticalFlow([old_gray], [old_gray], r, c, 15)
new_r, new_c = trackFeatures(old_gray, new_gray, np.copy(r), np.copy(c))


for i in range(len(new_r)):
    new_gray = cv2.arrowedLine(img, (c[i], r[i]), (new_c[i], new_r[i]), (0,0,1), thickness=1, tipLength=0.5)

cv2.imshow('f', new_gray)
cv2.waitKey(0)
