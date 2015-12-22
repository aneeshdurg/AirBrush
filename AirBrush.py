#Author: Aneesh Durg (durg2@illinois.edu)
#github.com/aneeshdurg/AirBrush
import cv2
import numpy as np
import pyautogui
import sys
import time
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
if __name__ == "__main__":
	controller = brush(cv2.VideoCapture(0))
	start = 0
	end = 0
	timer = False
	prevx, prevy = 0, 0

	debug = False
	show = False
	for i in range(1, len(sys.argv)):
		arg = sys.argv[i]
		if arg == '-a':
			debug = True
			show = True
			break
		elif arg == '-d':
			debug = True
		elif arg == '-v':
			show = True	
	
	while True:
		x, y = controller.getPos(show, debug)
		if not timer:
			start = time.time()
			timer = True
		try:
			pyautogui.moveTo(1920 - 3*x, 2*y)
		except:
			pass
		if abs(x-prevx) < 10 and abs(y-prevy) < 10:
			end = time.time()
			if end-start >= 3:
				try:
					pyautogui.click(1920 - 3*x,2*y)
				except:
					pass
				timer = False
		else:
			timer = False
			start = 0
		prevx = x
		prevy = y
