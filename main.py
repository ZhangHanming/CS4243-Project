import numpy as np
import cv2
from HarrisCorner import findCorners
from Draw import markWithCircle
from LucasKanade import trackFeatures

# Video Reader
cap = cv2.VideoCapture("Videos/traffic.mp4")

# Video Writer
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(
    'result.avi', 
    fourcc, 
    cap.get(cv2.CAP_PROP_FPS),
    (640, 480)
)

ret, old_frame = cap.read()
old_frame_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# Find corners on the first frame

r, c = findCorners(old_frame_gray, 11, 100)

cv2.imshow('frame', markWithCircle(r, c, old_frame))


while(1):
    ret, new_frame = cap.read()

    if(not ret):
        print "no frame to read"
        break

    new_frame_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

    r, c = trackFeatures(old_frame_gray, new_frame_gray, r, c)
    #cv2.imshow('frame', markWithCircle(r, c, new_frame))

    out.write(markWithCircle(r, c, new_frame))

    # break when ESC is pressed
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break

    old_frame = new_frame
    old_frame_gray = new_frame_gray



cv2.destroyAllWindows()
out.release()
cap.release()