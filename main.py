# Импортируем библиотеки cv2, time, numpy, и методы из модулей DetectionMethods и DrawingMethods
import cv2 as cv
import time
import numpy as np
import methods.DrawingMethods
import methods.MathematicalСalculationMethods
import math
import traceback

# Открываем видеопоток с камеры устройства под номером 0
cap = cv.VideoCapture(0)

# Если видеопоток не может быть открыт, вызываем исключение
if not cap.isOpened():
    raise Exception("Could not open video device")

# Инициализируем переменные start_time, frame_count, countCircles, countLines
start_time = time.time()
frame_count = 0
countCircles = 0
countLines = 0
simlines = None
avgRadius = 0

# Начинаем бесконечный цикл
while True:

    # Получаем очередной кадр с камеры
    ret, frame = cap.read()
    originalFrame = frame.copy()

    # Высота и ширина кадра
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Если кадр получить не удалось, выходим из цикла
    if not ret:
        break
        
    # Преобразуем кадр в черно-белый формат
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Применяем размытие Гаусса для сглаживания изображения
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Ищем окружности в изображении
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1,20, param1=70, param2=35, minRadius=5, maxRadius=100)

    #Проверяем, были ли обнаружены круги
    if circles is not None:
        #Вызываем метод DrawCircle из класса DrawingMethods, который рисует круги на изображении
        countCircles, newCircles = methods.DrawingMethods.DrawCircle(frame, circles)
        methods.DrawingMethods.DrawCircle(originalFrame, circles)


    # Применяем фильтр Канни для выделения краев
    canny = cv.Canny(gray, 50, 200, None, 3)
    
    # Определяем линии на изображении с помощью метода HoughLinesP
    lines = cv.HoughLinesP(canny, rho = 1, theta = np.pi/180, threshold = None, minLineLength = 50, maxLineGap = 10) 
    if lines is not None:
        for line in lines:
           x1,y1,x2,y2 = line[0]


    # Средний радиус окружности
    radius = (methods.MathematicalСalculationMethods.avgRadius(circles,countCircles))
    # Если обнаружены линии 
    if lines is not None:
        # Найти похожие линии с заданным порогом разницы
        simlines = methods.MathematicalСalculationMethods.findSimmilarLines(lines,2)
        if len(simlines) > 0:
            simLine = x1,y1,x2,y2
            x1,y1,x2,y2 = methods.MathematicalСalculationMethods.averageLineReturnsLine(simlines)
            try:
                # Получить коэфиценты линейного уравнения
                k, b = methods.MathematicalСalculationMethods.getLineEquation(x1,y1,x2,y2)
                x1 = 0
                y1 = int(k*x1+b)
                x2 = width
                y2 = int(k*x2+b)
                avgLine = x1,y1,x2,y2 

                P1 = np.array([x1, y1])
                P2 = np.array([x2, y2])
                # Получить массив всех точек на прямой
                pointsOfLine = methods.MathematicalСalculationMethods.createLineIterator(P1,P2,height,width)
                numberOfCrossings = 0
                arrayPointsOfLine = np.ndarray.tolist(pointsOfLine)

                # Если кий в правой части кадра, то необходимо перевернуть массив
                if methods.MathematicalСalculationMethods.needToReverse(arrayPointsOfLine,height,frame,originalFrame) == True:
                    pointsOfLine = sorted(pointsOfLine, key=lambda x: x[0], reverse=True)
                # Найдена ли окружность которая лежит на пути первой окружности
                isFoundSecondCrossing = False
                # Найдено ли первое пересечение
                isFoundFirstCrossing = False
                # Итерирование по точкам прямой
                for point in pointsOfLine:
                    if isFoundSecondCrossing == False:
                        # Получить цвета точки
                        b,g,r = originalFrame[point[1],point[0]]
                        # Если найдно пересечение
                        if g > 200 and r < 100 and b < 100:
                            #cv.putText(frame, 'detected', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv.LINE_AA)
                            numberOfCrossings += 1
                            # Если нашлось одно пересечение с первой окружностью, находим центр этой окружности и удаляем его
                            if numberOfCrossings > 0 and isFoundFirstCrossing == False:
                                minDist = 99999999
                                minCircleX = 0
                                minCircleY = 0
                                minCircleR = 0
                                # Ищем минимальное расстояние от точки пересечения до центра
                                for (x,y,r) in newCircles:
                                    distance = int(math.sqrt(abs((point[0]-x)**2) + abs((point[1]-y)**2)))
                                    if distance < minDist: 
                                        minDist = distance
                                        minCircleX = int(x)
                                        minCircleY = int(y)
                                        minCircleR = int(r)
                                newCircles.remove([minCircleX,minCircleY,minCircleR])
                                cv.circle(frame, (minCircleX, minCircleY), 40, (0, 0, 255), 2)
                                isFoundFirstCrossing = True
                        # Представляем, что шар летит дальше и находим точку на прямой, в которой будет находится центр 
                        # окружности, которая столкнется со второй окружностью (расстояние от этой точки до центра второй
                        # окружности равна диаметру)
                        if numberOfCrossings > 0:
                            x1,y1 = point[0],point[1] 
                            for (x2,y2,r) in newCircles:
                                if isFoundSecondCrossing == False:
                                    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                                    if abs(distance-2*radius) < 2*radius/20:
                                        #cv.putText(frame, 'bump', (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv.LINE_AA)
                                        cv.circle(frame, (x1, y1), int(radius), (0, 0, 255), 2)
                                        methods.DrawingMethods.DrawRay(frame,x1,y1,x2,y2,100)
                                        isFoundSecondCrossing = True
                                        break
                    # Отрисовываем прямую направления кия
                    cv.line(frame, (point[0], point[1]), (point[0], point[1]), (255, 0, 0), 1)                  
            except Exception as ex:
                print(traceback.format_exc())
                print(ex)

    # Отображаем изображение с кругами и линиями
    cv.imshow("Camera", frame)

    # Увеличиваем счетчик кадров
    frame_count += 1

    # Вычисляем прошедшее время
    elapsed_time = time.time() - start_time

    # Если прошло более 1 секунды
    if elapsed_time >= 1.0:
        # Вычисляем количество кадров в секунду
        fps = frame_count / elapsed_time
        # Выводим количество кадров в секунду, количество окружностей и линий
        print("Frames per second: {:.2f}".format(fps),"number of circles: ", countCircles, "number of lines: ", countLines)

        # Обновляем время и сбрасываем счетчик кадров
        start_time = time.time()
        frame_count = 0

    # Если нажата клавиша 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        # Выход
        break
# Освободить объект захвата
cap.release()

# Закрыть все окна 
cv.destroyAllWindows()
