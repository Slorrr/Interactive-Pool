import math
import cv2 as cv
import numpy as np
import methods.DrawingMethods

def findAngleFromPoints(x1,y1,x2,y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def findAngelFromLine(line):
    x1,y1,x2,y2 = line
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def findSimmilarLines(linesArray,maxDiff = 10):
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

def averageLineReturnsLine(image, lines):
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
