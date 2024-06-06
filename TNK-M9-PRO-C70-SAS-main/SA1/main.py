import cv2
from cvzone.HandTrackingModule import HandDetector

import pyautogui
import numpy as np


# Declare variable for width, height
# Width of Camera
width = 640
# Height of Camera
height = 480
# Frame Rate
frameR = 100
# Smoothening Factor
smoothening = 1

# Delecare the variables to store the screen sizes
screenSize = pyautogui.size()
screenWidth = screenSize[0]
screenHeight = screenSize[1]

# Previous coordinates
prevX = 0
prevY = 0

# Current coordinates
currX = 0
currY = 0

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)


while True:

    try:
        check, cameraFeedImg = cap.read()
        cameraFeedImg = cv2.flip(cameraFeedImg, 1)

        handsDetector = detector.findHands(cameraFeedImg, flipType=False)
        hands = handsDetector[0]
        cameraFeedImg = handsDetector[1]

        if hands:
            hand1 = hands[0]
            lmList = hand1["lmList"]
            handType = hand1["type"]

            fingers = detector.fingersUp(hand1)

            # Get the index finger tip x and y
            if len(lmList) > 0:
                indexFingerTipX = lmList[8][0]
                indexFingerTipY = lmList[8][1]

                # If index finger is up and middle finger is down
                if fingers[1] == 1 and fingers[2] == 0:

                    # Get the points between two known data points using interpolation technique
                    x3 = np.interp(indexFingerTipX,
                                   (frameR, width-frameR), (0, screenWidth))
                    y3 = np.interp(indexFingerTipY,
                                   (frameR, height-frameR), (0, screenHeight))

                    currX = prevX + (x3 - prevX)/smoothening
                    currY = prevY + (y3 - prevY) / smoothening

                    # Move the cursor
                    pyautogui.moveTo(currX, currY)

                    # Draw the circle on the tip of index finger
                    cv2.circle(cameraFeedImg, (indexFingerTipX, indexFingerTipY),
                               15, (0, 255, 0), cv2.FILLED)

                    prevX = currX
                    prevY = currY

    except Exception as e:
        print(e)

    cv2.imshow("Virtual Mouse", cameraFeedImg)
    cv2.waitKey(1)
