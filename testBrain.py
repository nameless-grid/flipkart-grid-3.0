import cv2
import cv2 as cv
import numpy as np


def getContours(image):
    contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    centres = []
    centres.clear()

    for cnt in contours:
        area = cv.contourArea(cnt)

        if minArea < area < maxArea:
            print()
            print("Area =", area)

            # detecting center points of the detected contours
            M = cv.moments(cnt)
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])

            centres.append([x, y])

            # Drawing the shapes that were detected
            # Syntax:- cv.drawContours(imgSrc,presentIterationNo,-1=for all detected contours,color,thickness)
            cv.drawContours(imgContour, cnt, -1, (255, 5, 5), 2)

            # Calculation of perimeter
            # syntax, srcLength(presentContour,isItClosedContour)
            peri = cv.arcLength(cnt, True)
            print("Perimeter =", peri)

            # Approximating the no of corner point
            # syntax, approxPolyDP(presentCnt,resolution,isClosed)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            objCorner = len(approx)
            print("Corner =", objCorner)

    return centres


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None,
                                               scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        # hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def moveForward(y):
    return y + step


def moveBackward(y):
    return y - step


def moveRight(x):
    return x + step


def moveLeft(x):
    return x - step


# def rotateLeft(x, y):

# constraints
minArea = 10
maxArea = 50000
step = 5

# # detect contours / pixels
# pathI = "Resources/path1.png"
# img = cv.imread(pathI)
# img = cv.resize(img, (647, 320))
# imgContour = img.copy()

pathV = "Resources/record.mp4"
cap = cv.VideoCapture(pathV)

# colors = [[82, 150, 183, 96, 255, 255],
#           [0, 112, 0, 20, 182, 255],
#           [21, 100, 255, 141, 255, 255],
#           [139, 112, 0, 179, 182, 255]]

colors = [[31, 135, 183, 112, 255, 255],
          [0, 116, 0, 20, 182, 255],
          [22, 163, 138, 113, 255, 255],
          [140, 112, 0, 152, 183, 255]]

loop_no = 0
flag = True
cx, cy, w, h = 0, 0, 20, 20
arrowColor = (255, 0, 0)
while flag:
    success, img = cap.read()
    img = cv.resize(img, (647, 320))
    imgContour = img.copy()
    hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    low_H = colors[loop_no][0]
    low_S = colors[loop_no][1]
    low_V = colors[loop_no][2]
    high_H = colors[loop_no][3]
    high_S = colors[loop_no][4]
    high_V = colors[loop_no][5]
    color_masked = cv.inRange(hsvImg, (low_H, low_S, low_V), (high_H, high_S, high_V))
    centers = getContours(color_masked)
    centers.sort()

    if loop_no < 2:
        start = centers[2]
        end = centers[1]
    else:
        start = centers[0]
        end = centers[1]

    if cx == 0 and cy == 0:
        cx, cy = start
        a1, b1, a2, b2 = cx, cy + w // 2, cx, cy + 2 * w

    cv.rectangle(imgContour, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2),
                 (255, 0, 255), cv.FILLED)

    cv2.arrowedLine(imgContour, (a1, b1), (a2, b2), arrowColor, thickness=3)

    if not(-step < end[0] - cx < step) or not(-step < end[1] - cy < step):
        if not(-step < end[1] - cy < step):
            cy = moveForward(cy)
            a1, b1, a2, b2 = cx, cy + w // 2, cx, cy + 2 * w
        elif -step < end[1] - cy < step and not(-step < cx < step) and cx - end[0] > 0:
            cx = moveLeft(cx)
            a1, b1, a2, b2 = cx - w // 2, cy, cx - 2 * w, cy
        else:
            cx = moveRight(cx)
            a1, b1, a2, b2 = cx + w // 2, cy, cx + 2 * w, cy
    else:
        if loop_no + 1 < 4:
            loop_no += 1
        cx, cy = 0, 0

    for c in centers:
        print(str(c[0]) + " " + str(c[1]))
    imgStack = stackImages(0.6, [img, hsvImg, color_masked])
    cv.imshow("Stack", imgStack)
    cv.imshow("ImageContour", imgContour)

    if cv.waitKey(100) & 0xFF == ord('q'):
        break
