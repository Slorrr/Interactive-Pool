import math
import cv2 as cv
import numpy as np
import methods.DrawingMethods
import copy

def findAngleFromPoints(x1,y1,x2,y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def findAngelFromLine(line):
    x1,y1,x2,y2 = line
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def findSimmilarLines(linesArray,maxDiff = 3):
    #Количество "похожих" отрезков
    avgCount = 0
    #Промежуточный массив отрезков 
    lines = []
    #Прямые с наибольшим кол-вом "похожих" отрезков
    maxLines = []

    for i in range(0,len(linesArray-1)):
        count = 0
        lines = []
        deg1 = findAngelFromLine(linesArray[i][0])
        if deg1 == 90 or deg1 == 180:
            break
        for j in range(0,len(linesArray)-1):
                deg2 = findAngelFromLine(linesArray[j][0])
                if deg2 == 90 or deg2 == 180:
                    break
                if (abs(deg1-deg2) < maxDiff) or (abs(deg1-deg2) > 360-maxDiff):
                    count += 1
                    lines.append(linesArray[j])
        if count > avgCount:
            avgCount = count
            maxLines = lines
    return maxLines

def averageLineReturnsLine(lines):
    x1_sum = 0
    y1_sum = 0
    x2_sum = 0
    y2_sum = 0
    for line in lines:
        x1,y1,x2,y2 = line[0]
        x1_sum += x1
        y1_sum += y1
        x2_sum += x2
        y2_sum += y2
    x1_avg = x1_sum // len(lines)
    y1_avg = y1_sum // len(lines)
    x2_avg = x2_sum // len(lines)
    y2_avg = y2_sum // len(lines)
    return(x1_avg,y1_avg,x2_avg,y2_avg)

def averageLineWithDraws(image, lines):
    x1_sum = 0
    y1_sum = 0
    x2_sum = 0
    y2_sum = 0
    for line in lines:
        x1,y1,x2,y2 = line[0]
        x1_sum += x1
        y1_sum += y1
        x2_sum += x2
        y2_sum += y2
    x1_avg = x1_sum // len(lines)
    y1_avg = y1_sum // len(lines)
    x2_avg = x2_sum // len(lines)
    y2_avg = y2_sum // len(lines)
    cv.line(image, (x1_avg, y1_avg), (x2_avg, y2_avg), (0, 0, 255), 2)

#slope = k
#intercept = b
#y = kx + b
def getLineEquation(x1,y1,x2,y2):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    return (slope, intercept)


def DistanceBetweenSegments(start1, end1, start2, end2):
    x1, y1 = start1
    x2, y2 = end1
    x3, y3 = start2
    x4, y4 = end2

    # Calculate the denominator in the formula
    denominator = ((x2 - x1) * (y4 - y3)) - ((y2 - y1) * (x4 - x3))

    # If the denominator is zero, the segments are parallel
    if denominator == 0:
        return None

    # Calculate the numerator in the formula
    numerator = ((y1 - y3) * (x4 - x3)) - ((x1 - x3) * (y4 - y3))

    # Calculate the fraction along the first segment
    ua = numerator / denominator

    # Calculate the fraction along the second segment
    ub = ((y1 - y3) + (ua * (y2 - y1))) / (y4 - y3)

    # Calculate the intersection point if the segments intersect
    x = x1 + (ua * (x2 - x1))
    y = y1 + (ua * (y2 - y1))

    # Calculate the distance between the segments if they intersect
    if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
        return math.sqrt((x1 - x)**2 + (y1 - y)**2)

    # Otherwise, return None
    return None

def extendLineToIntersection2(width, height, originalFrame, frame, line):
    x1,y1,x2,y2 = line
    #print(x1,y1,x2,y2)
    k,b = getLineEquation(x1,y1,x2,y2)
    #print(k,b)
    minusX = x1
    plusX = x1

    
    while True:
        if plusX+1 < width and k*(plusX+1)+b >= 0 and k*(plusX+1)+b <= height:
            plusX += 1
            plusY = int(k*plusX+b)
            fuckingFrame = copy.deepcopy(originalFrame)
            print(k,b)
            #r,g,b = fuckingFrame[int(k*plusX+b),plusX]
            cv.line(frame, (100, 100), (300, 500), (0, 0, 255), 10) 
            cv.line(frame, (x1,y1), (plusX,int(k*plusX+b)), (0, 0, 255), 2) 
            line = x1, y1, plusX, plusY
            #print(x1,y1,plusX,plusY)
            #print(r,g,b)
            #if r == 0 and g == 255 and b == 0:
            #    print("green")
            #    return plusX,plusY
        else:
            break
