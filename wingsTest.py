from addImage import addImage
import cv2
import numpy as np

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
# params for ShiTomasi corner detection
feature_params = dict(maxCorners=10000,
                      qualityLevel=0.3,
                      minDistance=3,
                      blockSize=5)
# Parameters for lucas kanade optical flow
lk_params = dict(winSize=(13, 13),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

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
        a, b = new.ravel()
        c, d = old.ravel()
        distance = np.sqrt((a - c)**2 + (b - d)**2)
        if(distance > 5):
            scale = distance / 10.0 if distance / 10.0 < 2 else 2.0
            angle = np.rad2deg(np.arctan2(a - c, b - d))
            frame = addImage(b, a, angle + 180, scale,
                             int(300 * scale), image, frame)
    img = frame
    cv2.imshow('frame', img)
    out.write(frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)
cv2.destroyAllWindows()
cap.release()
