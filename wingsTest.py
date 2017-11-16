from addImage import addImage
import cv2
import numpy as np
from HarrisCorner import findCorners

cap = cv2.VideoCapture('Videos/arm.mp4')
imagePath = "feather.jpg"
image = cv2.imread(imagePath, 1)
fourcc = cv2.VideoWriter_fourcc(*'IYUV')
out = cv2.VideoWriter(
    'feather.avi',
    fourcc,
    cap.get(cv2.CAP_PROP_FPS),
    (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
     int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
)
# Parameters for lucas kanade optical flow
lk_params = dict(winSize=(13, 13),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
r, c = findCorners(old_gray, 13, 1500)
p0 = np.zeros((1500,1,2),dtype=np.float32)
for i in range(1500):
    p0[i] = np.array([c[i],r[i]],dtype=np.float32)

while(1):
    ret, frame = cap.read()
    if(not ret):
        print "no frame to read"
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    # draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        random_grey_scale = np.random.uniform(0.5,1.0)
        new_image = (image * random_grey_scale).astype(np.uint8)
        # a, c are col; b, d are row
        a, b = new.ravel()
        c, d = old.ravel()
        distance = np.sqrt((a - c)**2 + (b - d)**2)
        if(distance > 3 and distance < 20):
            scale = distance / 5.0
            angle = np.rad2deg(np.arctan2(a - c, b - d)) + 180
            frame = addImage(b, a, angle, scale,
                             int(300 * scale), new_image, frame)
    cv2.imshow('frame', frame)
    out.write(frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)
cv2.destroyAllWindows()
cap.release()
out.release()
