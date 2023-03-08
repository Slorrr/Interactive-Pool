import cv2
import numpy as np

# Отрисовать массив отрезков
def DrawCircle(image, circles):
    circles = np.round(circles[0, :]).astype("int")
    newCircles = []
    try:
        if circles is not None:
        # Loop over the circles
            for (x, y, r) in circles:
                newCircles.append([x,y,r])
                # Draw the circle in the output image
                cv2.circle(image, (x, y), r, (0, 255, 0), 1)
                cv2.circle(image, (x, y), 0, (0, 0, 255), 2)
            countCircles = len(circles)
            return countCircles, newCircles
    except TypeError:
        pass

# Отрисовать массив отрезков
def DrawLines(image,lines):
    # Если отрезки обнаружены
    if lines is not None:
        # Итерация по массиву отрезков
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Отрисовка линий
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        countLines = len(lines)
        return countLines

# Отрисовать один отрезок
def DrawLine(image,line):
    x1, y1, x2, y2 = line
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Отрисовать луч
def DrawRay(image,x1,y1,x2,y2,length):
    direction = (x2 - x1, y2 - y1)

    # Вычислите конечную точку луча
    x3, y3 = int(x1 + length * direction[0]), int(y1 + length * direction[1])

    # Нарисуйте линию от начальной точки до конечной точки
    cv2.line(image, (x1, y1), (x3, y3), (255, 0, 0), thickness=2, lineType=cv2.LINE_AA)