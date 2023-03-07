# Импортируем библиотеки cv2, time, numpy, и методы из модулей DetectionMethods и DrawingMethods
import cv2 as cv
import time
import numpy as np
import methods.DrawingMethods
import methods.MathematicalСalculationMethods

# Открываем видеопоток с камеры устройства под номером 0
cap = cv.VideoCapture("video.mp4")

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
    #methods.MathematicalСalculationMethods.extendLineToIntersection(originalFrame)
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
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1,20, param1=70, param2=35, minRadius=5, maxRadius=50)

    #Проверяем, были ли обнаружены круги
    if circles is not None:
        #Вызываем метод DrawCircle из класса DrawingMethods, который рисует круги на изображении
        countCircles = methods.DrawingMethods.DrawCircle(frame, circles)
        methods.DrawingMethods.DrawCircle(originalFrame, circles)
        print(type(circles))
    sumRadius = 0
    for (x,y,r) in circles:
        sumRadius += r
    avgRadius = sumRadius / countCircles

    # Применяем фильтр Канни для выделения краев
    canny = cv.Canny(gray, 50, 200, None, 3)
    
    # Определяем линии на изображении с помощью метода HoughLinesP
    lines = cv.HoughLinesP(canny, rho = 1, theta = np.pi/180, threshold = None, minLineLength = 50, maxLineGap = 10) 
    if lines is not None:
        for line in lines:
           x1,y1,x2,y2 = line[0]
           #cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

    # Проверяем, были ли обнаружены линии
    #if lines is not None:
    #    simlines = methods.MathematicalСalculationMethods.findSimmilarLines(lines,2)
    #    # Вызываем метод DrawLine из класса DrawingMethods, который рисует линии на изображении
    #    countLines = methods.DrawingMethods.DrawLines(frame, simlines)
    
    if lines is not None and len(lines) > 0:
        simlines = methods.MathematicalСalculationMethods.findSimmilarLines(lines,2)
        if len(simlines) > 0:
            #methods.MathematicalСalculationMethods.averageLineWithDraws(frame, simlines)
            simLine = x1,y1,x2,y2
            x1,y1,x2,y2 = methods.MathematicalСalculationMethods.averageLineReturnsLine(simlines)
            try:
                k, b = methods.MathematicalСalculationMethods.getLineEquation(x1,y1,x2,y2)
                #print(x1,y1,x2,y2,k,b)
                x1 = 0
                y1 = int(k*x1+b)
                x2 = width
                y2 = int(k*x2+b)
                #print("start = ",x1,y1,"finish = ",x2,ye2)
                cv.line(frame,(x1,y1),(x2,y2),(255,0,0),2)
                avgLine = x1,y1,x2,y2

                #k,b = methods.MathematicalСalculationMethods.getLineEquation(x1,y1,x2,y2)
                #methods.MathematicalСalculationMethods.extendLineToIntersection2(width,height,originalFrame,frame,avgLine)
                P1 = np.array([x1, y1])
                P2 = np.array([x2, y2])
                a = methods.MathematicalСalculationMethods.createLineIterator(P1,P2,height,width)
                for i in a:
                    cv.line(frame, (i[0], i[1]), (i[0], i[1]), (255, 0, 255), 1)
                    b,g,r = originalFrame[i[1],i[0]]
                    if b == 0 and g == 255 and r == 0:
                        cv.putText(frame, 'detected', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv.LINE_AA)
            except Exception:
                #print(ex)
                pass

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
