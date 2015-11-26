#Author: Aneesh Durg (durg2@illinois.edu)
#github.com/aneeshdurg/AirBrush
import cv2
import numpy as np
class brush:
	#Video capture object
	cap = None
	x = 0
	y = 0
	
	def __init__(Self, cap):
		Self.cap = cap
	
	def getPos(Self, showScreen, debug):
		#get frame
		_, frame = Self.cap.read()
		#Converts frame to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		#Lower and upper bounds for yellow
		lower = np.array([20,20,20])
		upper = np.array([45,255,255])
		#Yellow mask (Grayscale)
		mask = cv2.inRange(hsv, lower, upper)
		res = cv2.bitwise_and(frame,frame, mask= mask)
		#Blob detection parameters
		params = cv2.SimpleBlobDetector_Params()
		params.filterByArea = 1
		params.minArea = 100
		params.filterByColor = 1
		params.blobColor = 0
		#Blob detector
		detector = cv2.SimpleBlobDetector(params)
		#Detected blobs
		keypoints = detector.detect(res)
		#Shows video with detected blobs
		if showScreen:
			im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
			cv2.imshow("Keypoints", im_with_keypoints)
		#Stores position in x, y
		for kpt in keypoints:
			if debug:
				print str(kpt.pt[0])+" "+str(kpt.pt[1])
			x =int(keypoints[0].pt[0])
			y =int(keypoints[0].pt[1])

		if len(keypoints)==0:
			if debug:
				print "Not found!"
			x, y = 0, 0
			
		return x, y	