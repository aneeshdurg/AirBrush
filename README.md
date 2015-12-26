# AirBrush as an importable class
Class to get coordinates from an airbrush

Requires OpenCV2, numpy

To use, import the class. See example:

>import AirBrush

Must be instantiated with a cv2 VideoCapture object. See example:

>cap = cv2.VideoCapture(0)

>myBrush = AirBrush.brush(cap=cap)

By default AirBrush searches for a yellow brush. To change the color of the brush set the 
B, G, R values as follows:

>myBrush = AirBrush.brush(cap=cap, B=<blue value>, G=<green value>, R=<red value>)

To use an image instead of video input, use the following:

>image = cv2.imread('path to image')

>myBrush = AirBrush.brush(frame=image)

x and y coordinates are obtained by the function getPos, which takes two booleans 
as parameters. The first boolean is to show or surpress video output, the second
for console output. The video output will show the frames captued, highlighting
the location of the brush. The console output will display the coordinates of the brush.
Note that the x coordinate will be inverted, depending on the way your video
input is given. X and Y coordinates will also be mapped to the bounds of the frames obtained from the video input, which can be obtained as follows:

>width(x-bound) = myBrush.width

>height(y-bound) = myBrush.height

The width and height instance variables are obatined by the cv2 functions:

>cap.get(3)

>cap.get(4)

If the pointer is not found, getPos will return (0, 0, False), otherwise returns (x, y, True) 
Note that errors in grabbing frames from the video input are ignored.

See example:

>while True:

>     x, y, found = myBrush.getPos(False, True)

For an example of a suitable AirBrush, see:

![Brush](http://i.imgur.com/K6bKWJx.jpg "Brush")

Sample usage can be seen at:
	
	https://github.com/aneeshdurg/AirPaint

#AirBrush as a mouse

Requires OpenCV, numpy, PyAutoGUI

AirBrush can also be launched by itself to use as a mouse. To launch, you can use the commands:
>AirBrush.py

>AirBrush.py -a

>AirBrush.py -d

>AirBrush.py -v

>AirBrush.py -c

>AirBrush.py -m(duration)

>AirBrush.py -m

The argument:

	-a 	prints the position of the pointer to the console and displays the video input with detected points.

	-d  prints the position of the pointer to the console.

	-v  displays the video input with detected points.

	-c Allows to specify the BGR values of the color of the brush being detected. Default is yellow.

	-m(duration) sets the click duration to (duration). Default is 3s.

	-m Prompts for click duration. Default is 3s.   

Holding the brush relatively still for 3 or more seconds sends a mouse left button click.

Holding the brush still for a further 3 seconds presses the left mouse button down.

Holding the brush still for a further 3 seconds afterwards releases the left mouse button.

The video input is taken from the first availible webcam (device id = 0).

TODO:

	Implement mouse right button click.