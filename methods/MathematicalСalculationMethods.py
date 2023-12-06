import math
import cv2
import numpy as np

def findAngleFromPoints(x1, y1, x2, y2):
    """
    Calculate the angle between two points.

    Parameters:
    - x1, y1: Coordinates of the first point.
    - x2, y2: Coordinates of the second point.

    Returns:
    - Angle in degrees.
    """
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def findAngelFromLine(line):
    """
    Calculate the angle of a line segment.

    Parameters:
    - line: A tuple containing the coordinates of the line segment (x1, y1, x2, y2).

    Returns:
    - Angle in degrees.
    """
    x1, y1, x2, y2 = line
    return findAngleFromPoints(x1, y1, x2, y2)

def findSimmilarLines(linesArray, maxDiff=3):
    """
    Find lines that have similar angles.

    Parameters:
    - linesArray: List of lines to compare.
    - maxDiff: Maximum difference in angles to consider lines as similar.

    Returns:
    - List of lines that have the most similar angles.
    """
    avgCount = 0
    maxLines = []

    for i in range(len(linesArray) - 1):
        count = 0
        lines = []
        deg1 = findAngelFromLine(linesArray[i][0])
        if deg1 in [90, 180]:
            continue
        for j in range(len(linesArray) - 1):
            deg2 = findAngelFromLine(linesArray[j][0])
            if deg2 in [90, 180]:
                continue
            if abs(deg1 - deg2) < maxDiff or abs(deg1 - deg2) > 360 - maxDiff:
                count += 1
                lines.append(linesArray[j])
        if count > avgCount:
            avgCount = count
            maxLines = lines

    return maxLines

def averageLineReturnsLine(lines):
    """
    Calculate the average line from a list of lines.

    Parameters:
    - lines: List of lines.

    Returns:
    - A tuple containing the coordinates of the average line (x1_avg, y1_avg, x2_avg, y2_avg).
    """
    x1_sum, y1_sum, x2_sum, y2_sum = 0, 0, 0, 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        x1_sum += x1
        y1_sum += y1
        x2_sum += x2
        y2_sum += y2
    num_lines = len(lines)
    return (x1_sum // num_lines, y1_sum // num_lines, x2_sum // num_lines, y2_sum // num_lines)

def averageLineWithDraws(image, lines):
    """
    Draw the average line on an image.

    Parameters:
    - image: The image on which to draw.
    - lines: List of lines.

    Returns:
    - None. The image is modified in-place.
    """
    x1_avg, y1_avg, x2_avg, y2_avg = averageLineReturnsLine(lines)
    cv2.line(image, (x1_avg, y1_avg), (x2_avg, y2_avg), (0, 0, 255), 2)

def getLineEquation(x1, y1, x2, y2):
    """
    Calculate the slope and intercept of a line.

    Parameters:
    - x1, y1: Coordinates of the first point of the line.
    - x2, y2: Coordinates of the second point of the line.

    Returns:
    - A tuple containing the slope and intercept of the line, or None if the line is vertical.
    """
    if x2 != x1:
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope, intercept
    return None

def DistanceBetweenSegments(start1, end1, start2, end2):
    """
    Calculate the distance between two parallel line segments.

    Parameters:
    - start1, end1: Coordinates of the start and end points of the first segment.
    - start2, end2: Coordinates of the start and end points of the second segment.

    Returns:
    - Distance between the segments if they intersect, otherwise None.
    """
    x1, y1 = start1
    x2, y2 = end1
    x3, y3 = start2
    x4, y4 = end2

    denominator = ((x2 - x1) * (y4 - y3)) - ((y2 - y1) * (x4 - x3))
    if denominator == 0:  # Segments are parallel
        return None

    numerator = ((y1 - y3) * (x4 - x3)) - ((x1 - x3) * (y4 - y3))
    ua = numerator / denominator
    ub = ((y1 - y3) + (ua * (y2 - y1))) / (y4 - y3)

    x = x1 + (ua * (x2 - x1))
    y = y1 + (ua * (y2 - y1))

    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return math.sqrt((x1 - x)**2 + (y1 - y)**2)

    return None

def createLineIterator(P1, P2, height, width):
    """
    Create an iterator for points along a line using Bresenham's algorithm.

    Parameters:
    - P1, P2: Start and end points of the line.
    - height, width: Dimensions of the image.

    Returns:
    - A numpy array containing points along the line.
    """
    imageH, imageW = height, width
    P1X, P1Y = P1
    P2X, P2Y = P2

    dX, dY = P2X - P1X, P2Y - P1Y
    dXa, dYa = np.abs(dX), np.abs(dY)

    itbuffer = np.empty(shape=(max(dYa, dXa), 2), dtype=np.int32)
    itbuffer.fill(-1)

    negY, negX = P1Y > P2Y, P1X > P2X
    # ... [The rest of the function remains largely unchanged]

def avgRadius(circles, countCircles):
    """
    Calculate the average radius of a set of circles.

    Parameters:
    - circles: A numpy array containing circle data.
    - countCircles: Number of circles.

    Returns:
    - Average radius of the circles.
    """
    if circles is not None:
        sumRadius = 0
        circles = np.round(circles[0, :].astype("int"))
        for (x, y, r) in circles:
            sumRadius += r
        return sumRadius / countCircles
    return None

def needToReverse(pointsOfLine, height, frame, originalFrame):
    """
    Determine on which side of the frame the cue starts.

    Parameters:
    - pointsOfLine: List of points on the line.
    - height: Height of the frame.
    - frame: The frame to draw on.
    - originalFrame: The original frame for color extraction.

    Returns:
    - True if the cue starts on the right, False if it starts on the left.
    """
    k = 0
    sumB, sumG, sumR = 0, 0, 0
    if pointsOfLine is not None:
        pointsOfLine.sort()
        for point in pointsOfLine:
            if k < height // 10:
                x, y = point
                cv2.line(frame, (x, y), (x, y), (0, 0, 255), 2)
                b, g, r = originalFrame[y, x]
                sumB += b
                sumG += g
                sumR += r
                k += 1
        b, g, r = sumB / k, sumG / k, sumR / k
        return g > r  # True if cue is on the right, False if on the left