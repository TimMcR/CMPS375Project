# boardReader is intended to take the most recent image of the game board and convert it an array.
# The array is 8x8x3, with dimensions corresponding to x coordinate, y coordinate, and occupation.
# Occupation codes are 0, 1, and 2 corresponding to empty, white piece, and black piece respectively.
# If you need anything related to this file, talk to Carter.

# Given an image (Working filename/path is just "boardImage.jpg"), processing occurs in steps:
# Step 1: Convert image to greyscale, then blur. Use thresholding to make black/white
# Step 2 (TO-DO): Detect outline of the chess board and crop along that outline
# Step 3: Sequentially detect the first threshold, going high y to low y, low x to high x
# Step 4: Determine the occupation status on the lower x side of the threshold
# Step 5: Repeat steps 4-6, until all squares have been recognized

import sys
import numpy as np
import cv2 as cv
from imutils import contours

# Image input
img = cv.imread("devImages/inkedCroppedBoardSmall.jpg")
oimg = img
cv.imwrite("imageOut/input.jpg", img)

# Colorspace + Blurring
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.GaussianBlur(img, (39,39), 6, 6)
cv.imwrite("imageOut/grayscale.jpg", img)

# Thresholding
img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
cv.imwrite("imageOut/threshBinary.jpg", img)

# Contours
cnts = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cv.drawContours(image= oimg, contours= cnts, contourIdx= -1, color= (0, 0, 255), thickness= 2, lineType= cv.LINE_AA)
cv.imwrite("imageOut/countours.jpg", oimg)
for c in cnts:
    area = cv.contourArea(c)
    if area < 1000:
        cv.drawContours(img, [c], -1, (0,0,0), -1)

# Fix boundaries
vertical_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,5))
img = cv.morphologyEx(img, cv.MORPH_CLOSE, vertical_kernel, iterations=9)
horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,1))
img = cv.morphologyEx(img, cv.MORPH_CLOSE, horizontal_kernel, iterations=4)

# Sort top -> bottom and left -> right
invert = 255 - img
cnts = cv.findContours(invert, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
if len(cnts) == 2:
    cnts = cnts[0] 
else:
    cnts = cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

chess_rows = []
row = []
for (i, c) in enumerate(cnts, 1):
    area = cv.contourArea(c)
    if area > 50000:
        row.append(c)
        if i % 9 == 0:
            (cnts, _) = contours.sort_contours(row, method="left-to-right")
            chess_rows.append(cnts)
            row = []

# Iterate through boxes
for row in chess_rows:
    for c in row:
        mask = np.zeros(img.shape, dtype=np.uint8)
        cv.drawContours(mask, [c], -1, (255,255,255), -1)
        result = cv.bitwise_and(image, mask)
        result[mask==0] = 255
        cv.imshow('result', result)
        cv.waitKey(175)

cv.imshow('img', img)
cv.imshow('invert', invert)
cv.waitKey()

#Image display, for development purposes
#cv.imshow("Image", img)
#cv.waitKey(0)
