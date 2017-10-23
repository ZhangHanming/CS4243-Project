import cv2

def markWithCircle(r, c, frame):
    for i in range(len(r)):
        frame = cv2.circle(frame, (c[i], r[i]), 5, (0, 0, 255), 1)

    return frame