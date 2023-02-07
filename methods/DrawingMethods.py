import cv2 as cv
import numpy as np

def DrawCircle(image, circles):
    circles = np.round(circles[0, :]).astype("int")
    try:
        if circles is not None:
        # Loop over the circles
            for (x, y, r) in circles:
                # Draw the circle in the output image
                cv.circle(image, (x, y), r, (0, 255, 0), 2)
                cv.circle(image, (x, y), 2, (0, 0, 255), 2)
            countCircles = len(circles)
            return countCircles
    except TypeError:
        pass

def DrawLine(image,lines):
    # Check if any lines were detected
    if lines is not None:
        # Loop over the lines
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Draw the line in the output image
            cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        countLines = len(lines)
        return countLines
    