import cv2
from cv2 import COLOR_BGR2GRAY
import numpy as np
import math 

#Shape detection using Canny and OpenCV
# use contours to find edges
#   - contours are groups of any connected edges

# cv2.arcLength(contour_car, True) returns perimeter of contour_var

# is knowing the number of sides enough?
# NOOO
# we use a ration to identify a shape
## sqrt(area) / perimeter
## use cv2.contourArea(contour_name) to get area of contour
## add import math first to use math.sqrt()
### for some reason subtracting 0.01 from ration helps to get accurate results
# quality of life functions
## stackImages: multiple images in the same window, good for testing
## showValue: shows values of params and allows you to adjust them

# task
## pick to detect a shape, triangle, square, rectangle, pentagon, hexagon, octagon, cross, star
## cover cicular shapes later, quarter circle

## challenge make one for a trapezoid
# requirements: shape detector cannot confuse other shapes with any of the other shapes above

#higher threshold leads to more strict contrasts required for edges
thresh1 = 100
thresh2 = 180

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()
    imgCan = cv2.Canny(img, thresh1, thresh2)
    kernel = np.ones((3,3))
    imgDil = cv2.dilate(imgCan, kernel, iterations = 1)

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cntr, heirarchy = cv2.findContours(imgDil.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for c in cntr:
        # gets length of contours
        peri=cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)
        
        #
        x,y,w,h = cv2.boundingRect(approx)
        
        # responsible for fetching amount of sides in contours
        sides = len(approx)
        area = cv2.contourArea(c)
        
        if (area > 500):
            cv2.putText(img, str(sides), (x + y - 100, y + 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0 ), 2)
            cv2.drawContours(img, c, -1, (255, 0, 0),7)
    cv2.imshow('img', img)
    k = cv2.waitKey(27) & 0xff
    if k == ord('q'):
        break
cv2.destroyAllWindows()
    