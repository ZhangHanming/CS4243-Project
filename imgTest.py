from rainbow import pasteImage
import cv2

img = cv2.imread("rainbow.png", -1)
dest = cv2.imread("flower_pot_gray.jpg", 1)
pos = [100, 100]
cv2.imshow("", pasteImage(img, dest, pos))
cv2.waitKey(0)
cv2.destroyAllWindows()
