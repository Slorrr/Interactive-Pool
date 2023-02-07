# Импортируем библиотеки cv2, time, numpy, и методы из модулей DetectionMethods и DrawingMethods
import cv2 as cv
import time
import numpy as np
import methods.DrawingMethods
import methods.MathematicalСalculationMethods

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

# Начинаем бесконечный цикл
while True:

    # Получаем очередной кадр с камеры
    ret, frame = cap.read()

    # Если кадр получить не удалось, выходим из цикла
    if not ret:
        break
        
    # Преобразуем кадр в черно-белый формат
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Применяем размытие Гаусса для сглаживания изображения
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Ищем окружности в изображении
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1,20, param1=90, param2=70, minRadius=1, maxRadius=100)

    # Проверяем, были ли обнаружены круги
    if circles is not None:
            # Вызываем метод DrawCircle из класса DrawingMethods, который рисует круги на изображении
            countCircles = methods.DrawingMethods.DrawCircle(frame, circles)

    # Применяем фильтр Канни для выделения краев
    canny = cv.Canny(gray, 50, 200, None, 3)
    # Определяем линии на изображении с помощью метода HoughLinesP
    lines = cv.HoughLinesP(canny, rho = 1, theta = np.pi/180, threshold = None, minLineLength = 50, maxLineGap = 10) 
    # Проверяем, были ли обнаружены линии
    if lines is not None:
        simlines = methods.MathematicalСalculationMethods.findSimmilarLines(lines,2)
        # Вызываем метод DrawLine из класса DrawingMethods, который рисует линии на изображении
        countLines = methods.DrawingMethods.DrawLine(frame, simlines)

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
