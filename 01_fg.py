import cv2 as cv
import numpy as np
import imutils
import urllib.request as add

# constraints
minArea = 10
maxArea = 50000

# detect contours / pixels
path = "resources/path1.png"
img = cv.imread(path)
img = cv.resize(img,(647,320))
imgContour = img.copy()

def currBotPos(bot):
    botMasked = cv.inRange(hsvImg,np.array(bots[bot][0:3]),np.array(bots[bot][3:6]))
    botPos = getContours(botMasked)

    print("bot current position")
    print(botPos)
    cv.circle(imgContour,botPos,10,(0,0,0),2)

    return botPos

def detectBot(bot):
    botMasked = cv.inRange(hsvImg,np.array(bots[bot][0:3]),np.array(bots[bot][3:6]))
    botPos = getContours(botMasked)

    # print("bot position available")
    # print(bot1Pos,bot2Pos,bot3Pos,bot4Pos)

    botSource = botPos[2]
    print("bot sources")
    print(botSource)
    cv.circle(imgContour,botSource,10,(0,0,0),2)
    
    botDest = botPos[0]
    print("bot destination")
    print(botDest)
    cv.circle(imgContour,botDest,10,(0,0,0),2)

    return [botMasked,botPos,botDest]


# Bot information
bots = {
        "bot1" : [28,0,0,140,255,255],
        "bot2" : [1,106,0,23,255,255],
        "bot3" : [24,163,0,179,255,255],
        "bot4" : [97,0,0,179,255,255]
    }

bot1 = detectBot('bot1')
bot1Source = bot1[1]
bot1Dest = bot1[2]

bot2 = detectBot('bot2')
bot2Source = bot2[1]
bot2Dest = bot2[2]

bot3 = detectBot('bot3')
bot3Source = bot3[1]
bot3Dest = bot3[2]

bot4 = detectBot('bot4')
bot4Source = bot4[1]
bot4Dest = bot4[2]


"""
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
"""

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
    contours = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    contours=imutils.grab_contours(contours)

    centres = []
    centres.clear()

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area>minArea and area<maxArea:
            print()
            print("Area =",area)

            # detecting center points of the detected contours
            M = cv.moments(cnt)
            cx=int(M['m10']/M['m00'])
            cy=int(M['m01']/M['m00'])

            centres.append([cx,cy])

            cv.circle(img,(cx,cy),3,(0,0,255),-1)

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

            # creating bounding box around the detected bot
            cv.boundingRect(approx)

    return centres

def show():
    imgStack = stackImages(0.6,([img,grayedImg,blurredImg],[canniedImg,imgContour,imgContour]))
    cv.imshow("stack",imgStack)

def start():

    #bot1
    move('bot1',1,bot1Dest[1]) #Move bot in y 1 direction
    turnLeft('bot1')
    move('bot1',0,bot1Dest[0]) #move bot in x 0 direction
    initDrop('bot1')
    stopDrop('bot1')
    # return back
    move('bot1',0,bot1Source[1]) #Move bot in y 1 direction
    turnLeft('bot1')
    move('bot1',1,bot1Source[0]) #move bot in x 0 direction

    #bot2
    move('bot2',1,bot2Dest[1]) #Move bot in y 1 direction
    turnLeft('bot2')
    move('bot2',0,bot2Dest[0]) #move bot in x 0 direction
    initDrop('bot2')
    stopDrop('bot2')
    # return back
    move('bot2',0,bot2Source[1]) #Move bot in y 1 direction
    turnLeft('bot2')
    move('bot2',1,bot2Source[0]) #move bot in x 0 direction

    #bot3
    move('bot3',1,bot1Dest[1]) #Move bot in y 1 direction
    turnLeft('bot3')
    move('bot3',0,bot1Dest[0]) #move bot in x 0 direction
    initDrop('bot3')
    stopDrop('bot3')
    # return back
    move('bot3',0,bot1Source[1]) #Move bot in y 1 direction
    turnLeft('bot3')
    move('bot3',1,bot1Source[0]) #move bot in x 0 direction

    #bot4
    move('bot4',1,bot1Dest[1]) #Move bot in y 1 direction
    turnLeft('bot4')
    move('bot4',0,bot1Dest[0]) #move bot in x 0 direction
    initDrop('bot4')
    stopDrop('bot4')
    # return back
    move('bot4',0,bot1Source[1]) #Move bot in y 1 direction
    turnLeft('bot4')
    move('bot4',1,bot1Source[0]) #move bot in x 0 direction

    

def move(bot,axis,destPos):
    currPos=currBotPos(bot)[axis]
    while(currPos!=destPos):
        add.urlopen('http://10.42.0.62/'+ bot +'moveForward')
        currPos=currBotPos(bot)
        show()
    stop()

def turnLeft(bot):
    add.urlopen('http://10.42.0.62/'+ bot +'turnLeft')
    show()

def turnRight(bot):
    add.urlopen('http://10.42.0.62/'+ bot +'turnRight')
    show()

def stop(bot):
    add.urlopen('http://10.42.0.62/'+ bot +'stop')
    show()

def initDrop(bot):
    add.urlopen('http://10.42.0.62/'+ bot +'initDrop')
    show()

def stopDrop(bot):
    add.urlopen('http://10.42.0.62/'+ bot +'stopDrop')
    show()


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

    #Start
    data = start()
    
    # Displaying all the images
    show(data)

    # waiting time
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
