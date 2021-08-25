import cv2 as cv
import numpy as np

# detect contours / pixels
path = "Resources/pathb.jpg"
img = cv.imread(path)
img = cv.resize(img, (647, 320))
imgContour = img.copy()

bot = [[122, 131, 169, 255, 58, 255],
       [0, 179, 176, 255, 47, 123],
       [7, 14, 0, 255, 0, 255],
       [59, 80, 0, 255, 51, 179]]

destination = [[28, 0, 0, 140, 255, 255],
               [1, 106, 0, 23, 255, 255],
               [24, 163, 0, 179, 255, 255],
               [97, 0, 0, 179, 255, 255]]

"""
bot = {
    'bot1': [122, 131, 169, 255, 58, 255],
    'bot2': [0, 179, 176, 255, 47, 123],
    'bot3': [7, 14, 0, 255, 0, 255],
    'bot4': [59, 80, 0, 255, 51, 179]
}

destination = {
    'dest1': [28, 0, 0, 140, 255, 255],
    'dest1': [1, 106, 0, 23, 255, 255],
    'dest1': [24, 163, 0, 179, 255, 255],
    'dest1': [97, 0, 0, 179, 255, 255]
}
"""


# Get contour function
def getContours(image):
    contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if 10 < area < 50000:
            print()
            print("Area =", area)
            # Drawing the shapes that were detected
            # syntax, drawContours(imgSrc,presentIterationNo,-1=for all detected contours,color,thickness)
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
        hor_con = [imageBlank] * rows
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


loop_no = 0
lower = np.array([bot[loop_no][0], bot[loop_no][1], bot[loop_no][2]])
upper = np.array([bot[loop_no][3], bot[loop_no][4], bot[loop_no][5]])
# low_H = bot[loop_no][0]
# low_S = bot[loop_no][1]
# low_V = bot[loop_no][2]
# high_H = bot[loop_no][3]
# high_S = bot[loop_no][4]
# high_V = bot[loop_no][5]
hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
bot_masked = cv.inRange(hsvImg, lower, upper)
cv.imshow("masked", bot_masked)
cv.waitKey(0)

# loop_no = 0
# while loop_no < 4:
#     grayedImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     blurredImg = cv.GaussianBlur(grayedImg, (19, 19), 0.5)
#     canniedImg = cv.Canny(blurredImg, 1000, 640)
#     hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#
#     low_H = bot[loop_no][0]
#     low_S = bot[loop_no][1]
#     low_V = bot[loop_no][2]
#     high_H = bot[loop_no][3]
#     high_S = bot[loop_no][4]
#     high_V = bot[loop_no][5]
#     bot_masked = cv.inRange(hsvImg, (low_H, low_S, low_V), (high_H, high_S, high_V))
#     cv.imshow("masked", bot_masked)
#     getContours(bot_masked)
#     imgStack = stackImages(0.6, [img, hsvImg, bot_masked])
#     cv.imshow("stack", imgStack)
#     cv.waitKey(0)
#     # waiting time
#     # if cv.waitKey(1) & 0xFF == ord('q'):
#     #     break
