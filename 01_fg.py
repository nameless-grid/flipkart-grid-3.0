import cv2 as cv
import numpy as np

# detect contours / pixels
path = "/media/deepaksagar/Study Materials/Flipkart_Grid3.O/resources/path1.png"
img = cv.imread(path)
img = cv.resize(img,(647,320))
imgContour = img.copy()


def empty(a):
    pass

# creating trackbars
cv.namedWindow("TrackBars")
cv.resizeWindow("TrackBars",640,100)
cv.createTrackbar("Hue Min", "TrackBars",0,179,empty)
cv.createTrackbar("Hue Max", "TrackBars",179,179,empty)
cv.createTrackbar("Sat Min", "TrackBars",203,255,empty)
cv.createTrackbar("Sat Max", "TrackBars",255,255,empty)
cv.createTrackbar("Val Min", "TrackBars",183,255,empty)
cv.createTrackbar("Val Max", "TrackBars",255,255,empty)


# Creating stack images function
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

# Get contour function
def getContours(img):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area>10 and area<50000:
            print()
            print("Area =",area)
            # Drawing the shapes that were detected
            # syntax, drawContours(imgSrc,presentIterationNo,-1=for all detected contours,color,thickness)
            cv.drawContours(imgContour,cnt,-1,(255,5,5),2)

            # Calculation of perimeter
            # syntax, srcLength(presentContour,isItClosedContour)
            peri = cv.arcLength(cnt,True)
            print("Perimeter =",peri)

            # Aproximating the no of cornor point
            # syntax, approxPolyDP(presntCnt,resolution,isClosed)
            approx = cv.approxPolyDP(cnt,0.02*peri,True)
            objCorner = len(approx)
            print("Corner =",objCorner)

def detectBot():
    bots = {
        "bot1" : [28,0,0,140,255,255],
        "bot2" : [1,106,0,23,255,255],
        "bot3" : [24,163,0,179,255,255],
        "bot4" : [97,0,0,179,255,255]
    }

    bot1Masked = cv.inRange(hsvImg,np.array(bots['bot1'][0:3]),np.array(bots['bot1'][3:6]))
    bot2Masked = cv.inRange(hsvImg,np.array(bots['bot2'][0:3]),np.array(bots['bot2'][3:6]))
    bot3Masked = cv.inRange(hsvImg,np.array(bots['bot3'][0:3]),np.array(bots['bot3'][3:6]))
    bot4Masked = cv.inRange(hsvImg,np.array(bots['bot4'][0:3]),np.array(bots['bot4'][3:6]))

    return [bot1Masked,bot2Masked,bot3Masked,bot4Masked];


while True:
    # Converting images to other form
    grayedImg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    blurredImg = cv.GaussianBlur(grayedImg,(19,19),0.5)
    canniedImg = cv.Canny(blurredImg,1000,640)
    hsvImg = cv.cvtColor(img,cv.COLOR_BGR2HSV)

    """
    # getting all the values from trackbars
    h_min = cv.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv.getTrackbarPos("Hue Max","TrackBars")
    s_min = cv.getTrackbarPos("Hue Min","TrackBars")
    s_max = cv.getTrackbarPos("Hue Max","TrackBars")
    v_min = cv.getTrackbarPos("Hue Min","TrackBars")
    v_max = cv.getTrackbarPos("Hue Max","TrackBars")

    # lower limit and upper limit for color detection
    ll = np.array([h_min,s_min,v_min])
    ul = np.array([h_max,s_max,v_max])
    print(ll,ul)
    """

    # create masked image
    bots = detectBot()

    # Displaying all the images
    getContours(canniedImg)
    imgStack = stackImages(0.6,([img,grayedImg,blurredImg],[canniedImg,imgContour,bots[1]],[bots[1],bots[2],bots[3]]))
    cv.imshow("stack",imgStack)

    # waiting time
    if cv.waitKey(1) & 0xFF == ord('q'):
        break