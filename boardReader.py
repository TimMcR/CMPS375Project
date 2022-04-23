#<<<<<<< HEAD

# boardReader is intended to take the most recent image of the game board and convert it an array.
# The array is 8x8x3, with dimensions corresponding to x coordinate, y coordinate, and occupation.

# boardReader is intended to take the most recent image of the game board and convert it an array.
# The array is 8x8x3, with dimensions corresponding to x coordinate, y coordinate, and occupation.
# Assumes that provided image is 1280x1280 pixels

import cv2
from imutils import contours
import numpy as np


# ++++++++++++++++++++++++++++++++++++++++++++
# +++++++Cropping game board from image+++++++
# ++++++++++++++++++++++++++++++++++++++++++++
# Load image, grayscale, and adaptive threshold
image = cv2.imread('devImages\decroppedBoard.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,12)
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Make all contours top level
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#Use area and number of sides of each contour to search for the board and white out all else
for (i, c) in enumerate(cnts, 1):
    area = cv2.contourArea(c)
    #If area is > 300,000 (~547x547 pixels, or ~20% of the image's total area), to ensure we're not picking up individual squares
    if area > 300000:
        #If area is < 1,000,000 (1000x1000 pixels, or ~60% of the image's total area), to ensure it's not a just a table or something
        if area < 1000000:
            approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c,True), True)
            print("Side count: ", str(len(approx)))
            #If the shape is a quadrilateral
            if len(approx) == 4:
                n = approx.ravel()
                q = 0
                cropXMax = 0
                cropYMax = 0
                cropXMin = 10000
                cropYMin = 10000
                for j in n:
                    if (q % 2 == 0):
                        if (n[q] > cropXMax):
                            cropXMax = n[q]
                        if (n[q] < cropXMin):
                            cropXMin = n[q]
                        if (n[q+1] > cropYMax):
                            cropYMax = n[q+1]
                        if (n[q+1] < cropYMin):
                            cropYMin = n[q+1]
                    q = q + 1
                #cv2.line(image,(cropXMin,cropYMin), (cropXMax,cropYMax), (255,0,0), 10)
                #cv2.imwrite("imageOut\cropDimensions.png", image)
                image = image[cropYMin:cropYMax, cropXMin:cropXMax]
                image = cv2.resize(image, (1000,1000))
                cv2.imwrite("imageOut\cropped.png", image)
                print("Image cropped")
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,15,12)
                cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if len(cnts) == 2 else cnts[1]


# ++++++++++++++++++++++++++++++++++++++++++++
# +++++Splitting cropped image into boxes+++++
# ++++++++++++++++++++++++++++++++++++++++++++
#Thicken lines
for c in cnts:
    area = cv2.contourArea(c)
    if area < 7000:
        cv2.drawContours(thresh, [c], -1, (0,0,0), -1)
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
    if area < 90000:
        if area > 5000:
            row.append(c)
            if i % 8 == 0:  
                (cnts, _) = contours.sort_contours(row, method="left-to-right")
                chess_rows.append(cnts)
                row = []


# ++++++++++++++++++++++++++++++++++++++++++++
# ++++++++Image detection within boxes++++++++
# ++++++++++++++++++++++++++++++++++++++++++++
# Note: High accuracy template lists have been commented out as they have proven cumbersome time-wise.
# Abridged lists have been provided for live demonstration. Restoring full accuracy will massively increase required time.
compositeResult = np.zeros(image.shape, dtype=np.uint8)
oList = []
# Making list of templates to match
#templateList120 = []
templateList100 = []
#templateList80 = []
templateList60 = []
fileNames1 = ["king", "queen", "qbishop", "qrook", "knight", "pawn"]
#fileNames2 = ["0d", "9d", "18d", "27d", "36d", "45d", "54d", "63d", "72d", "81d"]
fileNames2 = ["0d", "9d"]
for fn1 in fileNames1:
    for fn2 in fileNames2:
        templateList100.append(cv2.imread("templates\\"+fn1+fn2+".png"))
for tmps in templateList100:
    #templateList120.append(cv2.resize(tmps, (120,120)))
    #templateList80.append(cv2.resize(tmps, (80,80)))
    templateList60.append(cv2.resize(tmps, (60,60)))
#tmpsLists = [templateList120, templateList100, templateList80, templateList60]
tmpsLists = [templateList100, templateList60]
#Matching each individual square against all templates until a good match is found or all templates have been examined
for row in chess_rows:
    for c in row:
        # Isolate the square
        mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [c], -1, (255,255,255), -1)
        result = cv2.bitwise_and(image, mask)
        # Match templates
        bestMatch = 0
        for tmpsList in tmpsLists:
            for tmps in tmpsList:
                if bestMatch > 0.3:
                    continue
                currMatch = cv2.matchTemplate(result, tmps, cv2.TM_CCOEFF_NORMED)
                (__, maxVal, __, __) = cv2.minMaxLoc(currMatch)
                if maxVal > bestMatch:
                    bestMatch = maxVal
        print(str(bestMatch))
        # Mark space as occupied if a good match was found
        if bestMatch > 0.3:
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
listSizeGap = 64 - len(oList)
while listSizeGap > 0:
    oList.append(0)
    listSizeGap = listSizeGap - 1
aList = np.array(oList).reshape(8,8)
print(str(aList))
# Un-comment to run
#read("devImages/inkedCroppedBoard.jpg")
#>>>>>>> 8daca53742d8e81d7b040fea98e0324cf8069057
