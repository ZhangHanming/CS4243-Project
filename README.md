# CS4243-Project

Python Version: 2.7.12 (64-bit)

OpenCV Version: 3.3.0 (64-bit)

Numpy Version: 1.13

To track corners:

1. Specify video path at line 10 in main.py
2. run  `python main.py`
3. the result video is at 'Videos/track.avi'

To create special effect video:

1. Specify video path at line 10 in main.py
2. run `python main.py`
3. run `python wings.py`
4. the result video is at 'Videos/wing.avi' 

Files:
1. HarrisCorner.py - Funtion to find corners
2. LucasKanade.py - Lucas Kanade tracker
3. addImage.py - Funtion to paste one imgae on another
4. main.py - script to track corners of a video and save the coordinates as `cols.csv` and `rows.csv`
5. wings.py - script to add wings to a video
6. cv2.pyd - cv2 lib file
