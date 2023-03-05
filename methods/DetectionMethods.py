from cv2 import cv2
import numpy as np


def HoughLinesP(image, rho = 1, theta = np.pi/180, threshold = None, minLineLength = 100, maxLineGap = 10):
    # Detect lines in the image using HoughLinesP
    cannyImage = cv2.Canny(image, 50, 200, None, 3)
    lines = cv2.HoughLinesP(cannyImage, rho, theta, threshold, minLineLength, maxLineGap)
    return lines
