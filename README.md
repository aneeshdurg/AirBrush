# AirBrush as an importable class
Class to get coordinates from an airbrush

Requires OpenCV2, numpy, pyautogui

To use, import the class. See example:

>import AirBrush

Must be instantiated with a cv2 VideoCapture object. See example:

>cap = cv2.VideoCapture(0)

>brush = AirBrush.brush(cap)

x and y coordinates are obtained by the function getPos, which takes two booleans 
as parameters. The first boolean is to show or surpress video output, the second
for console output. The video output will show the frames captued, highlighting
the location of the brush. The console output will display the coordinates of the brush.
Note that the x coordinate will probably be inverted, depending on the way your video
input is given. X and Y coordinates will also be mapped to an arbitrary scale, depending on the video input.

If the pointer is not found, getPos will return (0, 0) to avoid unwanted errors

See example:

>while True:

>     x, y = getPos(False, True)

For an example of a suitable AirBrush, see:

![Brush](http://i.imgur.com/K6bKWJx.jpg "Brush")

Sample usage can be seen at:
	
	https://github.com/aneeshdurg/AirPaint

#AirBrush as a mouse
AirBrush can also be launched by itself to use as a mouse. To launch, you can use the commands:
>AirBrush.py
>AirBrush.py -a
>AirBrush.py -d
>AirBrush.py -v

The argument:
	-a 	prints the position of the pointer to the console and displays the video input with detected points
	-d  prints the position of the pointer to the console
	-v  displays the video input with detected points

Holding the brush relatively still for 3 or more seconds sends a mouse click.
The video input is taken from the first availible webcam.




