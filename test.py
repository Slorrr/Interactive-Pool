import numpy as np
import cv2 as cv
from methods import MathematicalСalculationMethods

# Create a black image
height = 512
width = 512
img = np.zeros((height,width,3), np.uint8)
# Draw a diagonal blue line with thickness of 5 px
cv.line(img,(256,256),(512,512),(255,0,0),5)


while True:
	cv.imshow("test",img)
	print(MathematicalСalculationMethods.findAngle(256,256,512,512))
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cv.destroyAllWindows()