#Author: Aneesh Durg (durg2@illinois.edu)
#github.com/aneeshdurg/AirBrush
import cv2
import numpy as np
import math
class brush:
	#Video capture object
	cap = None
	prevx = None
	prevy = None
	color = None

	def __init__(Self, cap, B, G, R):
		Self.cap = cap
		color = np.uint8([[[B, G, R]]])
		Self.color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)[0][0][0]

	def dist(Self, pt):
		return math.sqrt(math.pow(pt[0]-Self.prevx, 2)+math.pow(pt[1]-Self.prevy, 2))

	def getPos(Self, showScreen, debug):
		if Self.prevx == None:
			Self.prevx = Self.cap.get(3)/2
			Self.prevy = Self.cap.get(4)/2
		#get frame
		_, frame = Self.cap.read()
		#Converts frame to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		#Lower and upper bounds for yellow
		lower = np.array([Self.color-10,20,20])
		upper = np.array([Self.color+10,255,255])
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

		found = True
		if len(keypoints)==0:
			if debug:
				print "Not found!"
			x, y = 0, 0
			found = False
			return x, y, found

		#Stores position in x, y
		low = 0
		for i in range(1, len(keypoints)):
			if Self.dist(keypoints[low].pt) > Self.dist(keypoints[i].pt):
				low = i
		
		x =int(keypoints[low].pt[0])
		y =int(keypoints[low].pt[1])

		if debug:
			print x+" "+y
		
		Self.prevx = x
		Self.prevy = y
		return x, y, found	

if __name__ == "__main__":

	import pyautogui
	import sys
	import time
	
	debug = False
	show = False
	changeColor = False
	for i in range(1, len(sys.argv)):
		arg = sys.argv[i]
		if arg == '-a':
			debug = True
			show = True
		elif arg == '-d':
			debug = True
		elif arg == '-v':
			show = True	
		elif arg == '-c':
			b = int(raw_input("B: "))
			g = int(raw_input("G: ")) 
			r = int(raw_input("R: "))
			changeColor = True
	
	pyautogui.FAILSAFE = False
	if changeColor:
		controller = brush(cv2.VideoCapture(0), b, g, r)
	else:
		controller = brush(cv2.VideoCapture(0), 0, 255, 255)	
	start = 0
	end = 0
	timer = False
	prevx, prevy = 0, 0

	while True:
		x, y, found = controller.getPos(show, debug)
			
		if not timer:
			start = time.time()
			timer = True

		if found:
			pyautogui.moveTo(1920 - 3*x, 2*y)

		if abs(x-prevx) < 10 and abs(y-prevy) < 10:
			end = time.time()
			if end-start >= 3:
				pyautogui.click(1920 - 3*x,2*y)
				timer = False
		else:
			timer = False
			start = 0
		prevx = x
		prevy = y
		cv2.waitKey(30)