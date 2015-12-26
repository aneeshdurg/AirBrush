#Author: Aneesh Durg (durg2@illinois.edu)
#github.com/aneeshdurg/AirBrush
import cv2
import numpy as np
import math
class brush:
	#Video capture object
	cap = None
	frame = None
	prevx = None
	prevy = None
	color = None
	width = 0
	height = 0

	def __init__(Self, **kwargs):
		if 'B' not in kwargs:
			B = 0
		else:
			B = kwargs['B']

		if 'G' not in kwargs:
			G = 255
		else:
			G = kwargs['G']

		if 'R' not in kwargs:
			R = 255
		else:
			R = kwargs['R']		

		if 'cap' in kwargs:
			Self.cap = kwargs['cap']
		elif frame in kwargs:
			Self.frame = kwargs['frame']
			if Self.frame is None:
				raise ValueError('Invalid file path!')
		else:
			raise ValueError('Incorrect arguments!')

		color = np.uint8([[[B, G, R]]])
		Self.color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)[0][0][0]
		if 'cap' in kwargs:
			Self.width = Self.cap.get(3)
			Self.height = Self.cap.get(4)
		else:
			Self.width = Self.frame.shape[1]
			Self.height = Self.frame.shape[0]	

	def dist(Self, pt):
		return math.sqrt(math.pow(pt[0]-Self.prevx, 2)+math.pow(pt[1]-Self.prevy, 2))

	def getPos(Self, showScreen, debug):
		if Self.prevx == None:
			Self.prevx = Self.cap.get(3)/2
			Self.prevy = Self.cap.get(4)/2
		#get frame
		if Self.cap is not None:
			_, frame = Self.cap.read()
		else:
			frame = Self.frame
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
			im_with_keypoints = cv2.flip(im_with_keypoints, 1)
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
			print str(x)+" "+str(y)
		
		Self.prevx = x
		Self.prevy = y
		return x, y, found	

if __name__ == "__main__":
	#imports required only for mouse
	import pyautogui
	import sys
	import time
	#variables
	pyautogui.FAILSAFE = False
	size = [pyautogui.size()[0], pyautogui.size()[1]]
	hold = [False, False]
	start = 0
	end = 0
	timer = False
	prevx, prevy = 0, 0
	screenX, screenY = 0, 0
	#variables modifiable by arguments
	debug = False
	show = False
	changeColor = False
	click = 3
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
		elif arg[:2] == '-m':
			if len(arg) > 2:
				click = int(arg[2:])
			else:
				click = int(raw_input("Click duration: "))	
	#brush object				
	if changeColor:
		controller = brush(cap=cv2.VideoCapture(0), B=b, G=g, R=r)
	else:
		controller = brush(cap=cv2.VideoCapture(0))	
	#main loop
	while True:
		#Getting x y position of pointer
		x, y, found = controller.getPos(show, debug)
		#timer for clicks	
		if not timer:
			start = time.time()
			timer = True
		#moves cursor	
		if found:
			screenX = size[0] - int(size[0]/controller.width)*x
			screenY = int(size[1]/controller.height)*y
			pyautogui.moveTo(screenX, screenY)
		#Clicking and draging	
		if abs(x-prevx) < 10 and abs(y-prevy) < 10:
			end = time.time()
			#Press left button 
			if end-start >= click and hold[0]:
				timer = False
				pyautogui.mouseDown(screenX, screenY, button='left')
				hold[1] = True
				hold[0] = False
			#Release left button
			elif end-start >= click and hold[1]:
				timer = False
				pyautogui.mouseUp(screenX, screenY, button='left')
				hold[1] = False	
			#Click left button
			elif end-start >= click:
				pyautogui.click(screenX, screenY)
				timer = False
				hold[0] = True
				hold[1] = False
		#If the timer's conditions are not satisfied, reset variables		
		else:
			timer = False
			hold[0] = False
			hold[1] = False
			start = 0
		#Update previous values
		prevx = x
		prevy = y

		cv2.waitKey(30)