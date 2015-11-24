# AirBrush
Class to get coordinates from an airbrush

Requires OpenCV2, numpy

Must be instantiated with a cv2 VideoCapture object. See example:

>cap = cv2.VideoCapture(0)

>brush = AirBrush.brush(cap)

x and y coordinates are obtained by the function getPos, which takes two booleans 
as parameters. The first boolean is to show or surpress video output, the second
for console output. The video output will show the frames captued, highlighting
the location of the brush. The console output will display the coordinates of the brush.
Note that the x coordinate will probably be inverted, depending on the way your video
input is given. X and Y coordinates will also be mapped to an arbitrary scale, depending on the video input.

See example:

>while True:

>     x, y = getPos(False, True)
