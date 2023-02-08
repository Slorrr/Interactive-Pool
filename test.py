import numpy as np
import cv2 as cv
import math
from methods import MathematicalСalculationMethods


def distance_between_parallel_segments(start1, end1, start2, end2):
    x1, y1 = start1
    x2, y2 = end1
    x3, y3 = start2
    x4, y4 = end2

    # Calculate the denominator in the formula
    denominator = ((x2 - x1) * (y4 - y3)) - ((y2 - y1) * (x4 - x3))

    # If the denominator is not zero, the segments are not parallel
    if denominator != 0:
        return None

    # Calculate the perpendicular distance from the start of the first segment to the line defined by the second segment
    numerator = ((y1 - y3) * (x4 - x3)) - ((x1 - x3) * (y4 - y3))
    distance = abs(numerator) / math.sqrt((x4 - x3)**2 + (y4 - y3)**2)

    return distance


start1 = (5,1)
end1 = (1,5)
start2 = (10,1)
end2 = (1,10)
print(distance_between_parallel_segments(start1,end1,start2,end2))
# Create a black image
#height = 512
#width = 512
#img = np.zeros((height,width,3), np.uint8)
## Draw a diagonal blue line with thickness of 5 px
#cv.line(img,(256,256),(512,512),(255,0,0),5)


#while True:
#	cv.imshow("test",img)
#	print(MathematicalСalculationMethods.findAngle(256,256,512,512))
#	if cv.waitKey(1) & 0xFF == ord('q'):
#		break
#
#cv.destroyAllWindows()