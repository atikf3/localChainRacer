#!/usr/bin/env python
import numpy as np
import cv2

print ('Loading camera') 
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('videoplayback.mp4')
cap.set(3, 160)
cap.set(4, 120)

print ('Starting racer')
while(cap.isOpened()):
    ret, frame = cap.read()
    #cv2.imshow('frame', frame)
    crop_img = frame[60:120, 0:160]
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    lower_or = np.array([10, 80, 40])
    upper_or = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_or, upper_or) 
    #gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(mask,(5,5),0)
    ret,thresh = cv2.threshold(blur,160,175,cv2.THRESH_BINARY)
    _, contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
 
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
 
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
 
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
 
        if cx >= 120:
            print ("L")
 
        if cx < 120 and cx > 50:
            print ("MID")
 
        if cx <= 50:
            print ("R")

    else:
        print ("No line")
 
    #Display the resulting frame
    cv2.imshow('preview',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
