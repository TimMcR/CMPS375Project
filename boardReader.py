# boardReader is intended to take the most recent image of the game board and convert it an array.
# The array is 8x8x3, with dimensions corresponding to x coordinate, y coordinate, and occupation.
# Occupation codes are 0, 1, and 2 corresponding to empty, white piece, and black piece respectively.
# If you need anything related to this file, talk to Carter.

# Given an image (Working filename/path is just "boardImage.jpg"), processing occurs in steps:
# Step 1: Convert image to greyscale
# Step 2: Apply gaussian blur
# Step 3: Detect outline of the chess board
# Step 4: Crop along that outline
# Step 5: Sequentially detect the first threshold, going low x to high x before low y to high y
# Step 6: Determine the occupation status on the lower x side of the threshold
# Step 7: Record the occupation status in the array output[n%8][n/8][occupation]
# Step 8: Repeat steps 5-7, ignoring the first n detections. Continue until n = 64

import sys
import cv2 as cv

# Image to be converted. Change to whatever the porper file path ends up being.
img = cv.imread("boardImage.jpg")

# Grayscale conversion of the original, which is then blurred. Second parameter of GaussianBlur changes how blurry it is. Odd numbers only.
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.GaussianBlur(img, (3,3), 0)

cv.imshow("Blurry gray", img)
cv.waitKey(0)