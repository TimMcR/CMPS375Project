# boardReader is intended to take the most recent image of the game board and convert it an array.
# The array is 8x8x3, with dimensions corresponding to x coordinate, y coordinate, and occupation.
# Occupation codes are 0, 1, and 2 corresponding to empty, white piece, and black piece respectively.
# If you need anything related to this file, talk to Carter.

# Given an image (Working filename/path is just "boardImage.jpg"), processing occurs in steps:
# Step 1: Convert image to greyscale
# Step 2: Detect outline of the chess board
# Step 3: Crop along that outline
# Step 4: Sequentially detect the first threshold, going low x to high x before low y to high y
# Step 5: Determine the occupation status on the lower x side of the threshold
# Step 6: Record the occupation status in the array output[n%8][n/8][occupation]
# Step 7: Repeat steps 4-6, ignoring the first n detections. Continue until n = 64

# Possible ways to improve accuracy: 
# Taking multiple pictures per step and taking the clearest
# Using R, G, and B masks and comparing seperately as opposed to a single greyscale mask


import sys
import cv2 as cv
from cv2 import THRESH_BINARY

# Image to be converted. Change to whatever the porper file path ends up being.
img = cv.imread("boardImage.jpg")
cv.imwrite("imageOut/input.jpg", img)

# Step 1
# UNUSED: Second parameter of GaussianBlur changes how blurry it is. Odd numbers only.
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imwrite("imageOut/grayscale.jpg", img)
#img = cv.GaussianBlur(img, (3,3), 0)

#Step 2:
img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 101, 2)
cv.imwrite("imageOut/threshBinary.jpg", img)
contours, hierarchy = cv.findContours(image = img, mode = cv.RETR_TREE, method = cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(image = img, contours = contours, contourIdx = -1, color = (0, 255, 0), thickness = 2, lineType = cv.LINE_AA)
cv.imwrite("imageOut/countours.jpg", img)

#Image display, for development purposes
cv.imshow("Image", img)
cv.waitKey(0)