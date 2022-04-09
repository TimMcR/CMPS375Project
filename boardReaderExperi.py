# boardReader is intended to take the most recent image of the game board and convert it an array.
# The array is 8x8x3, with dimensions corresponding to x coordinate, y coordinate, and occupation.
# Occupation codes are 0, 1, and 2 corresponding to empty, white piece, and black piece respectively.
# If you need anything related to this file, talk to Carter.

# Given an image, processing occurs in steps:
# Step 1: Convert image to greyscale, then blur. Use thresholding to make black/white
# Step 2 (TO-DO): Detect outline of the chess board and crop along that outline
# Step 3: Sequentially detect the first threshold, going high y to low y, low x to high x
# Step 4: Determine the occupation status on the lower x side of the threshold
# Step 5: Repeat steps 3 + 4 until all squares have been recognized

import cv2
from imutils import contours
import numpy as np

# Load image, grayscale, and adaptive threshold
image = cv2.imread('devImages\inkedCroppedBoardSmallSample.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)

# Filter out all noise to isolate only boxes
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 1000:
        cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

# Fix horizontal and vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

# Sort by top to bottom and each row by left to right
invert = 255 - thresh
cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

chess_rows = []
row = []
for (i, c) in enumerate(cnts, 1):
    area = cv2.contourArea(c)
    if area < 50000:
        row.append(c)
        if i % 9 == 0:  
            (cnts, _) = contours.sort_contours(row, method="left-to-right")
            chess_rows.append(cnts)
            row = []

# Image detection within box
sqList = [[image]*8]*8
sqLT = 0
sqLC = 0
for row in chess_rows:
    for c in row:
        mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [c], -1, (255,255,255), -1)
        result = cv2.bitwise_and(image, mask)
        result[mask==0] = 255
        if (sqLC > 7):
            sqLC = 0
            sqLT += 1
        if (sqLT != 8):
            sqList[sqLC][7 - sqLT]
            sqLC += 1
        #cv2.imshow('result', result)
        #cv2.waitKey(175)
temps = ["templates\pawn.jpg", "templates\king.jpg", "templates\knight.jpg", "templates\qbishop.jpg", "templates\qrook.jpg", "templates\queen.jpg"]
oList = [[0]*8]*8
for x in range(len(oList)):
    for y in range(len(oList[x])):
        for t in range(len(temps)):
            temp = cv2.imread(temps[t])
            res = cv2.matchTemplate(sqList[x][y], temp, cv2.TM_CCOEFF_NORMED)
            if (np.amax(res) >= 0.8):
                oList[x][y] = 1

cv2.imshow('thresh', thresh)
cv2.imshow('invert', invert)
cv2.waitKey()
print(str(oList))