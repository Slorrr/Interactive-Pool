import cv2
import numpy as np

def houghlinesp(image, rho=1, theta=np.pi/180, threshold=None, min_line_length=100, max_line_gap=1):
    """
    Detects lines in the given image using the Hough Line Transform method.

    Parameters:
    - image (numpy.ndarray): The input image on which line detection will be performed.
    - rho (float, optional): Resolution of the accumulator in pixels. Default is 1.
    - theta (float, optional): Angle resolution of the accumulator in radians. Default is np.pi/180.
    - threshold (int, optional): Accumulator threshold parameter. Only those lines are returned that get enough votes. Default is None.
    - min_line_length (int, optional): Minimum line length. Line segments shorter than this are rejected. Default is 100.
    - max_line_gap (int, optional): Maximum allowed gap between line segments to treat them as a single line. Default is 1.

    Returns:
    - lines (list): A list of lines detected in the image. Each line is represented by a 4-element vector (x1, y1, x2, y2).
    """
    
    # Apply the Canny edge detection on the image
    canny_image = cv2.Canny(image, 50, 200, None, 3)
    
    # Detect lines in the edge-detected image using HoughLinesP
    lines = cv2.HoughLinesP(canny_image, rho, theta, threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
    
    return lines
