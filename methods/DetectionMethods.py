import cv2 as cv
import numpy as np


def HoughLinesP(image, rho = 1, theta = np.pi/180, threshold = None, minLineLength = 100, maxLineGap = 10):
    # Detect lines in the image using HoughLinesP
    cannyImage = cv.Canny(image, 50, 200, None, 3)
    lines = cv.HoughLinesP(cannyImage, rho, theta, threshold, minLineLength, maxLineGap)
    return lines
