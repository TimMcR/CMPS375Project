# boardReader is intended to take the most recent image of the game board and convert it an array.
# The array is 8x8x3, with dimensions corresponding to x coordinate, y coordinate, and occupation.

import cv2
from imutils import contours
import numpy as np

# Load image, grayscale, and adaptive threshold
image = cv2.imread('devImages\croppedRealBoard4.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,12)


# Filter out all noise to isolate only boxes
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 1000:
        cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

# Use a mask to ensure we only look at the chess board
#for (i, c) in enumerate(cnts, 1):
#    area = cv2.contourArea(c)
#    if area > 30000:
#        cropMask = np.zeros(image.shape, dtype=np.uint8)
#        cv2.drawContours(cropMask, [c], -1, (255,255,255), -1)
#        image = cv2.bitwise_and(cropMask, image)

# Fix horizontal and vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

#Sort the contours from top-to-bottom, take the top 8, then sort them left-to-right
invert = 255 - thresh
cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
chess_rows = []
row = []
for (i, c) in enumerate(cnts, 1):
    area = cv2.contourArea(c)
    if area < 30000:
        if area > 4000:
            row.append(c)
            if i % 8 == 0:  
                (cnts, _) = contours.sort_contours(row, method="left-to-right")
                chess_rows.append(cnts)
                row = []


# Image detection within box
compositeResult = np.zeros(image.shape, dtype=np.uint8)
#temps = [cv2.imread("templates\pawnSmall.png"), cv2.imread("templates\kingSmall.png"), cv2.imread("templates\knightSmall.png"), cv2.imread("templates\qbishopSmall.png"), cv2.imread("templates\qrookSmall.png"), cv2.imread("templates\queenSmall.png")]
oList = []
phTemp = cv2.imread("templates\knightSmall.png")

for row in chess_rows:
    for c in row:
        # Isolate the square
        mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [c], -1, (255,255,255), -1)
        result = cv2.bitwise_and(image, mask)
        #Do template matching in the square
        #match = 0
        #for t in temps:
        #    temp = cv2.imread(t)
        #    templateResult = cv2.matchTemplate(result, temp, cv2.TM_CCOEFF_NORMED)
        #    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(templateResult)
        #    if maxVal > 0.5:
        #        print("Match found")
        #        match = 1
        #if match == 1:
        #    oList.append(1)
        #else:
        #    oList.append(0)
        templateResult = cv2.matchTemplate(result, phTemp, cv2.TM_CCOEFF_NORMED)
        (__, maxVal, __, __) = cv2.minMaxLoc(templateResult)
        print(str(maxVal))
        if maxVal > 0.3:
            oList.append(1)
        else:
            oList.append(0)
        cv2.imshow('result', result)
        compositeResult = compositeResult + result
        cv2.waitKey(50)
cv2.imshow('Composite Result', compositeResult)
cv2.waitKey(1000)
cv2.imwrite('imageOut\Othresh.png', thresh)
cv2.imwrite('imageOut\invert.png', invert)
cv2.imwrite('imageOut\composite.png', compositeResult)
aList = np.array(oList).reshape(8,8)
print(str(aList))