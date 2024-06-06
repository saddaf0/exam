import cv2
from cvzone.HandTrackingModule import HandDetector

import pyautogui
import numpy as np
import math


width = 640
height = 480
frameR = 100
smoothening = 1


screenSize = pyautogui.size()
screenWidth = screenSize[0]
screenHeight = screenSize[1]

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

            if len(lmList) > 0:
                indexFingerTipX = lmList[8][0]
                indexFingerTipY = lmList[8][1]

                # Get the middle finger tip x and y
                middleFingerTipX = lmList[12][0]
                middleFingerTipY = lmList[12][1]

                if fingers[1] == 1 and fingers[2] == 0:

                    x3 = np.interp(indexFingerTipX,
                                   (frameR, width-frameR), (0, screenWidth))
                    y3 = np.interp(indexFingerTipY,
                                   (frameR, height-frameR), (0, screenHeight))

                    currX = prevX + (x3 - prevX)/smoothening
                    currY = prevY + (y3 - prevY) / smoothening

                    pyautogui.moveTo(currX, currY)

                    cv2.circle(cameraFeedImg, (indexFingerTipX, indexFingerTipY),
                               15, (0, 255, 0), cv2.FILLED)

                    prevX = currX
                    prevY = currY

                # If index finger & middle finger both are up
                if fingers[1] == 1 and fingers[2] == 1:
                    distance = math.dist(lmList[8], lmList[12])

                    indexFingerTipX = lmList[8][0]
                    indexFingerTipY = lmList[8][1]
                    middleFingerTipX = lmList[12][0]
                    middleFingerTipY = lmList[12][1]

                    # Get the center point of the two fingers
                    cx = (indexFingerTipX + middleFingerTipX) // 2
                    cy = (indexFingerTipY + middleFingerTipY) // 2

                    # Draw the line between two fingers
                    cv2.line(cameraFeedImg, (indexFingerTipX, indexFingerTipY),
                             (middleFingerTipX, middleFingerTipY), (255, 0, 255), 2)

                    # If both fingers are really close to each other
                    if distance < 20:
                        print(distance)
                        cv2.circle(cameraFeedImg, (cx, cy),
                                   15, (0, 255, 0), cv2.FILLED)
                        # Perform Click
                        pyautogui.click()

    except Exception as e:
        print(e)

    cv2.imshow("Virtual Mouse", cameraFeedImg)
    cv2.waitKey(1)
