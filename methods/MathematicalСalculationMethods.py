import math
import cv2
import numpy as np

# Найти угол между точками
def findAngleFromPoints(x1,y1,x2,y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

# Найти угол отрезка
def findAngelFromLine(line):
    x1,y1,x2,y2 = line
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

# Найти "похожие" отрезки
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
                # Сравниваем углы двух отрезков с заданной погрешностью
                if (abs(deg1-deg2) < maxDiff) or (abs(deg1-deg2) > 360-maxDiff):
                    count += 1
                    lines.append(linesArray[j])
        if count > avgCount:
            avgCount = count
            maxLines = lines
    return maxLines

# Найти "среднюю" линию
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

# Найти "среднюю" линию и отрисовать ее
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

# Найти коэффиценты линейного уравнения
def getLineEquation(x1,y1,x2,y2):
    try:
        if (x2 - x1) != 0:
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            return (slope, intercept)
    except Exception:
        pass

# Найти расстояние между параллельными отрезками
def DistanceBetweenSegments(start1, end1, start2, end2):
    x1, y1 = start1
    x2, y2 = end1
    x3, y3 = start2
    x4, y4 = end2

    # Вычисление знаменателя в формуле
    denominator = ((x2 - x1) * (y4 - y3)) - ((y2 - y1) * (x4 - x3))

    # Если знаменатель равен нулю, то отрезки параллельны
    if denominator == 0:
        return None

    # Вычисление числителя в формуле
    numerator = ((y1 - y3) * (x4 - x3)) - ((x1 - x3) * (y4 - y3))

    # Вычисление дроби вдоль первого сегмента
    ua = numerator / denominator

    # Вычисление дроби вдоль второго сегмента
    ub = ((y1 - y3) + (ua * (y2 - y1))) / (y4 - y3)

    # Вычисление точки пересечения, если отрезки пересекаются
    x = x1 + (ua * (x2 - x1))
    y = y1 + (ua * (y2 - y1))

    # Вычисление расстояния между сегментами, если они пересекаются
    if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
        return math.sqrt((x1 - x)**2 + (y1 - y)**2)

    return None

def createLineIterator(P1, P2, height, width):
    imageH = height
    imageW = width
    P1X = P1[0]
    P1Y = P1[1]
    P2X = P2[0]
    P2Y = P2[1]

    # Разница и абсолютная разница между точками
    # используется для расчета наклона и относительного расположения между точками
    dX = P2X - P1X
    dY = P2Y - P1Y
    dXa = np.abs(dX)
    dYa = np.abs(dY)

    # Предопределить массив numpy для вывода на основе расстояния между точками
    itbuffer = np.empty(shape=(np.maximum(dYa,dXa),2),dtype=np.int32)
    itbuffer.fill(-1)

    # Получить координаты вдоль линии, используя форму алгоритма Брезенхэма
    negY = P1Y > P2Y
    negX = P1X > P2X
    if P1X == P2X: # Вертикальный отрезок
       itbuffer[:,0] = P1X
       if negY:
           itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
       else:
           itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)              
    elif P1Y == P2Y: # Горизонтальный отрезок
       itbuffer[:,1] = P1Y
       if negX:
           itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
       else:
           itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
    else: # Диогональный отрезок
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

    # Удалить точки вне кадра
    colX = itbuffer[:,0]
    colY = itbuffer[:,1]
    mask = (colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)
    itbuffer = itbuffer[mask]
    return itbuffer

# Найти средний радиус
def avgRadius (circles, countCircles):
    if circles is not None:
        sumRadius = 0
        circles = np.round(circles[0, :].astype("int"))
        try:
            if circles is not None:
                for (x,y,r) in circles:
                    sumRadius += r
            return sumRadius / countCircles
        except Exception:
            pass

# Определить в какой сторны кадра начинается кий
def needToReverse(pointsOfLine, height, frame,originalFrame):
    k = 0
    sumB = 0
    sumG = 0
    sumR = 0
    if pointsOfLine is not None:
        pointsOfLine.sort()
        for point in pointsOfLine:
            if k < int(height/10):
                x,y = point[0],point[1]
                cv2.line(frame, (x, y), (x, y), (0, 0, 255), 2)
                b,g,r = originalFrame[y,x]
                sumB += b
                sumG += g
                sumR += r
                k += 1
        b = sumB / k
        g = sumG / k
        r = sumR / k
        if g > r:
            # Кий справа
            return True
        else:
            # Кий слева
            return False