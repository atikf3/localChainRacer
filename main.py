#!/usr/bin/env python
import numpy as np
import cv2
import car_dir
import video_dir
import motor
import RPi.GPIO as GPIO

print ('Loading camera')
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('videoplayback.mp4')
cap.set(3, 160)
cap.set(4, 120)

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor.
car_dir.home()
print ('Starting racer')
motor.forward()
motor.setSpeed(30)
while(cap.isOpened()):
    ret, frame = cap.read()
    #cv2.imshow('frame', frame)
    crop_img = frame
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    lower_or = np.array([0, 40, 40])
    upper_or = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_or, upper_or)
    #gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(mask,(5,5),0)
    ret,thresh = cv2.threshold(blur,160,175,cv2.THRESH_BINARY)
    _, contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M['m00'] == 0.0 : 
            M['m00'] += 1
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

        if cx >= 120:
            car_dir.turn_right()
            motor.forward()
            motor.setSpeed(24)
            print ("L")

        if cx < 120 and cx > 50:
            car_dir.home()
            motor.setSpeed(24)
            motor.forward()

        if cx <= 50:
            car_dir.turn_left()
            motor.forward()
            motor.setSpeed(24)
            print ("R")

    else:
        motor.setSpeed(24)
        #motor.backward()
        motor.forward()
        print ("No line")

    #Display the resulting frame
    cv2.imshow('preview',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        motor.stop()
        break

motor.stop()