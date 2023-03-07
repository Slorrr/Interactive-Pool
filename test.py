import numpy as np
from cv2 import cv2 
import math
from methods import MathematicalСalculationMethods


def extendLineToIntersection(width, height, frame, line):
    x1, y1, x2, y2 = line
    k, b = MathematicalСalculationMethods.getLineEquation(x1, y1, x2, y2)
    minusX = x1
    plusX = x1
    while True:
        if minusX - 1 >= 0:
            if k * minusX + b <= height and k * minusX + b >= 0:
                minusX -= 1
                y = k * minusX + b

                print("minus point", minusX, k * minusX + b)
                print("plusX", plusX, "y", y)
                b, g, r = frame[plusX, int(y)]
                if (b, g, r) == (0, 255, 0):
                    print("KAAAAAAAAAAIF")
        if plusX + 1 <= width:
            if k * plusX + b <= height and k * plusX + b >= 0:
                plusX += 1
                y = k * plusX + b
                qweqw
                print("plus point", plusX, k * plusX + b)
                print("minus", minusX, k * minusX + b)

                b, g, r = frame[minusX, int(y)]
                if (b, g, r) == (0, 255, 0):
                    print("KAAAAAAAAAAIF")

    cv2.line(frame, (int(minusX), int(k * minusX + b)), (int(plusX, int(k * plusX + b)), (255, 255, 255), 2))

cap=cv2.VideoCapture(0)
ret, frame=cap.read()



# Create a black image
height=512
width=512
img=np.zeros((height, width, 3), np.uint8)
# Draw a diagonal blue line with thickness of 5 px
# cv2.line(img,(256,256),(512,512),(255,0,0),5)

line=50, 100, 100, 150
x1, y1, x2, y2=line

while True:
	cv2.imshow("test", frame)
	# print(MathematicalСalculationMethods.findAngle(256,256,512,512))

	extendLineToIntersection(width, height, frame, line)

	cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
