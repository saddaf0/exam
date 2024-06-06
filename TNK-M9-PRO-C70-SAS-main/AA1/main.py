import cvzone
import cv2
import math
from cvzone.HandTrackingModule import HandDetector

import pyautogui
import time
import numpy as np

width = 640
height = 480
frameR = 100
smoothening = 1
prevX = 0
prevY = 0
currX = 0
currY = 0
screenshot_num = 1
screenSize = pyautogui.size()
screenWidth = screenSize[0]
screenHeight = screenSize[1]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

while True:

    try:
        success, cameraFeedImg = cap.read()
        cameraFeedImg = cv2.flip(cameraFeedImg, 1)

        handsDetector = detector.findHands(cameraFeedImg, flipType=False)
        hands = handsDetector[0]
        cameraFeedImg = handsDetector[1]

        if hands:
            hand1 = hands[0]
            lmList = hand1["lmList"]  # List of 21 Landmark points
            bbox = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint = hand1['center']  # center of the hand cx,cy
            handType = hand1["type"]  # Handtype Left or Right
            fingers = detector.fingersUp(hand1)

            if len(lmList) > 0:
                x1 = lmList[8][0]
                y1 = lmList[8][1]

                if fingers[1] == 1 and fingers[2] == 0:
                    x3 = np.interp(x1, (frameR, width-frameR),
                                   (0, screenWidth))
                    y3 = np.interp(y1, (frameR, height-frameR),
                                   (0, screenHeight))

                    currX = prevX + (x3 - prevX)/smoothening
                    currY = prevY + (y3 - prevY) / smoothening

                    pyautogui.moveTo(currX, currY)
                    cv2.circle(cameraFeedImg, (x1, y1), 7,
                               (255, 0, 255), cv2.FILLED)
                    prevX, prevY = currX, currY

                if fingers[1] == 1 and fingers[2] == 1:
                    length = math.dist(lmList[8], lmList[12])

                    x1 = lmList[8][0]
                    y1 = lmList[8][1]
                    x2 = lmList[12][0]
                    y2 = lmList[12][1]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                    cv2.line(cameraFeedImg, (x1, y1),
                             (x2, y2), (255, 0, 255), 2)

                    if length < 20:
                        cv2.circle(cameraFeedImg, (cx, cy),
                                   15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()

                    print(length)
                    # Perform a right click if distance between index and middle finger is greater than 100
                    if length > 100:
                        cv2.circle(cameraFeedImg, (cx, cy),
                                   15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click(button='right')

                if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    screenshot_path = f'screenshots/screenshot_{screenshot_num}.png'
                    pyautogui.screenshot(screenshot_path)
                    screenshot_num += 1
                    print(f'Screenshot saved at {screenshot_path}')
                    time.sleep(1)

                if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    time.sleep(.1)
                    pyautogui.scroll(300)

                if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    time.sleep(.1)
                    pyautogui.scroll(-300)

    except Exception as e:
        print(e)

    cv2.imshow("Image", cameraFeedImg)
    cv2.waitKey(1)
