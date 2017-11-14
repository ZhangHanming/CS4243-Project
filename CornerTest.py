import sys
import cv2
import numpy as np
from rainbow import addEffect

# Video Reader
vPath = "Videos/mouse.mp4"
img = "rainbow.png"
cols = np.loadtxt("cols.csv", delimiter=",")
rows = np.loadtxt("rows.csv", delimiter=",")
addEffect(vPath, img, rows, cols)
