import math

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
        for j in range(0,len(linesArray)-1):
                deg2 = findAngelFromLine(linesArray[j][0])
                if (abs(deg1-deg2) < maxDiff) or (abs(deg1-deg2) > 360-maxDiff):
                    count += 1
                    lines.append(linesArray[j])
        if count > avgCount:
            avgCount = count
            maxLines = lines
    return maxLines

