import numpy as np
import cv2
import platform
from HarrisCorner import findCorners
from Draw import markWithCircle
from LucasKanade import trackFeatures


# Video Reader
cap = cv2.VideoCapture("Videos/sx.mp4")

# Video Writer
fourcc = cv2.VideoWriter_fourcc(*'IYUV')

out = cv2.VideoWriter(
    'result.avi',
    fourcc,
    cap.get(cv2.CAP_PROP_FPS),
    (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
     int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
)

ret, old_frame = cap.read()
frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
old_frame_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

corner_num = 180
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
row_list = np.zeros((corner_num, frame_count))
col_list = np.zeros((corner_num, frame_count))

# Find corners on the first frame
r, c = findCorners(old_frame_gray, 13, corner_num)
row_list[:, frame_num] = r
col_list[:, frame_num] = c

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

while(1):
    ret, new_frame = cap.read()

    if(not ret):
        print "no frame to read"
        break

    new_frame_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

    r_new, c_new = trackFeatures(old_frame_gray, new_frame_gray, r, c)
    row_list[:, int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1] = r_new
    col_list[:, int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1] = c_new
    #cv2.imshow('frame', markWithCircle(r, c, new_frame))
    for i in range(len(r)):
        mask = cv2.line(mask, (c_new[i],r_new[i]),(c[i],r[i]),color[i%100].tolist(),2)
        new_frame = cv2.circle(new_frame, (c_new[i],r_new[i]), 5, color[i%100].tolist(), -1)
    img = cv2.add(new_frame, mask)
    out.write(img)

    # break when ESC is pressed
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break

    old_frame = new_frame
    old_frame_gray = new_frame_gray
    r = r_new
    c = c_new

np.savetxt("rows.csv", row_list, delimiter=",")
np.savetxt("cols.csv", col_list, delimiter=",")

cv2.destroyAllWindows()
out.release()
cap.release()
