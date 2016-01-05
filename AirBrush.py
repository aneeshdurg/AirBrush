#Author: Aneesh Durg (durg2@illinois.edu)
#github.com/aneeshdurg/AirBrush
import cv2
import numpy as np
import math
import time
class brush:
	#Video capture object
	cap = None
	frame = None
	prevx = None
	prevy = None
	color = None
	width = 0
	height = 0
	pClick = False
	sClick = False
	clicked = False
	timer = False
	start = 0
	end = 0

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
		elif 'frame' in kwargs:
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

	def getClicked(Self, click=3, dist=10):
		x, y, found = Self.getPos(False, False)
		if found:
			if abs(x-Self.prevx) < dist and abs(y-Self.prevy) < dist:
				Self.end = time.time()
				#Secondary click 
				if Self.end-Self.start >= click and Self.clicked:
					Self.timer = False
					Self.pClick = False
					Self.sClick = True
					Self.clicked = False
				#primary click
				elif Self.end-Self.start >= click:
					Self.pClick = True
					Self.sClick = False
					Self.timer = False
					Self.clicked = True
			#If the timer's conditions are not satisfied, reset variables		
			else:
				Self.timer = False
				Self.pClick = False
				Self.sClick = False
				Self.start = 0
			return (Self.pClick, Self.sClick)	
		else:
			return (False, False)	


	def getPos(Self, showScreen, debug):
		if not Self.timer:
			Self.start = time.time()
			Self.timer = True
		
		if Self.prevx == None:
			Self.prevx = Self.width/2
			Self.prevy = Self.height/2
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
		if not found:
			Self.timer = False
			Self.start = 0

		return x, y, found	

if __name__ == "__main__":
	#imports required only for mouse
	import pyautogui
	import sys
	#variables
	pyautogui.FAILSAFE = False
	size = [pyautogui.size()[0], pyautogui.size()[1]]
	hold = False
	pClick, sClick = False, False
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
	cDist = 10
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
		elif arg[:2] = '-b':
			if len(arg) > 2:
				cDist = int(arg[2:])
			else:
				cDist = int(raw_input("Click error bound: "))	
				
	#brush object				
	if changeColor:
		controller = brush(cap=cv2.VideoCapture(0), B=b, G=g, R=r)
	else:
		controller = brush(cap=cv2.VideoCapture(0))	
	#main loop
	while True:
		#Getting x y position of pointer
		x, y, found = controller.getPos(show, debug)
		pClick, sClick = False, False
		if found:
			pClick, sClick = controller.getClicked(click = click, dist = cDist)
			if pClick:
				print 'pClick'
			if sClick:	
				print 'sClick'
		if not found:
			print '-'*10
		#timer for clicks	
		if not timer:
			start = time.time()
			timer = True
		#moves cursor	
		if found:
			screenX = size[0] - int(size[0]/controller.width)*x
			screenY = int(size[1]/controller.height)*y
			pyautogui.moveTo(screenX, screenY)
		
		if pClick and not hold:
			pyautogui.click(screenX, screenY)
			hold = True	
		elif sClick:
			pyautogui.mouseDown(screenX, screenY)
		elif pClick and hold:
			pyautogui.mouseUp(screenX, screenY)	
		#Update previous values
		prevx = x
		prevy = y

		cv2.waitKey(30)