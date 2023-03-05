import math
import cv2
import copy
import numpy as np

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
    cv2.line(image, (x1_avg, y1_avg), (x2_avg, y2_avg), (0, 0, 255), 2)

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



def createLineIterator(P1, P2, height, width):
   #define local variables for readability
   imageH = height
   imageW = width
   P1X = P1[0]
   P1Y = P1[1]
   P2X = P2[0]
   P2Y = P2[1]

   #difference and absolute difference between points
   #used to calculate slope and relative location between points
   dX = P2X - P1X
   dY = P2Y - P1Y
   dXa = np.abs(dX)
   dYa = np.abs(dY)

   #predefine numpy array for output based on distance between points
   itbuffer = np.empty(shape=(np.maximum(dYa,dXa),2),dtype=np.int32)
   itbuffer.fill(-1)

   #Obtain coordinates along the line using a form of Bresenham's algorithm
   negY = P1Y > P2Y
   negX = P1X > P2X
   if P1X == P2X: #vertical line segment
       itbuffer[:,0] = P1X
       if negY:
           itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
       else:
           itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)              
   elif P1Y == P2Y: #horizontal line segment
       itbuffer[:,1] = P1Y
       if negX:
           itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
       else:
           itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
   else: #diagonal line segment
       steepSlope = dYa > dXa
       if steepSlope:
           slope = dX.astype(np.float32)/dY.astype(np.float32)
           if negY:
               itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
           else:
               itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
           itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(int) + P1X
       else:
           slope = dY.astype(np.float32)/dX.astype(np.float32)
           if negX:
               itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
           else:
               itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
           itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(int) + P1Y

   #Remove points outside of image
   colX = itbuffer[:,0]
   colY = itbuffer[:,1]
   mask = (colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)
   itbuffer = itbuffer[mask]

   return itbuffer


def extendLineToIntersection2(width, height, originalFrame, frame, line):
    x1,y1,x2,y2 = line
    #print(x1,y1,x2,y2)
    k,b = getLineEquation(x1,y1,x2,y2)
    #print(k,b)
    plusX = x1
    
    ###
    #while True:
    #    if plusX+1 < width:
    #        plusX += 1
    #        plusY = round(k*plusX)+int(b)
    #        flag = False
    #        #print(str(width),str(plusX), str(height), str(plusY))
    #        #fuckingFrame = copy.deepcopy(originalFrame)
    #        #print(k,b)
    #        #r,g,b = fuckingFrame[int(k*plusX+b),plusX]
    #        if plusY < 480:
    #            b,g,r = originalFrame[plusY,plusX]
    #            cv2.line(frame,(plusX,plusY),(plusX,plusY),(255,0,0),2)
    #            if g == 255 and r == 0 and b == 0:
    #                print("PIIIIIIIIIIIIVVVVVOOOOOOO")
    #                print("PIIIIIIIIIIIIVVVVVOOOOOOO")
    #                print("PIIIIIIIIIIIIVVVVVOOOOOOO")
    #                print("PIIIIIIIIIIIIVVVVVOOOOOOO")
    #                flag = True
    #                cv2.putText(frame, 'YEAH', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    coordinates = []

    num_points = max(x2,x1) - min(x2,x1)

    x_values = [x1 + (x2 - x1) * i / (num_points - 1) for i in range(num_points)]
    y_values = [y1 + (y2 - y1) * i / (num_points - 1) for i in range(num_points)]

    for i in range(num_points):
        b,g,r = originalFrame[y_values[i],x_values[i]]
        if b == 0 and g == 255 and r == 255:
            cv2.putText(frame, 'YEAH', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    #else:
    #    break
