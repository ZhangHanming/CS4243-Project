from addImage import addImage
import cv2

image = cv2.imread("feather.jpg", 1)
bg = cv2.imread("flower_pot_gray.jpg", 1)

cv2.imshow("", addImage(400, 500, 90, 1.8, int(300 * 1.8), image, bg))
cv2.waitKey(0)
cv2.destroyAllWindows()
