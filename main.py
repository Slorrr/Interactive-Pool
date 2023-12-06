import cv2 as cv
import time
import numpy as np
import math
import traceback
from methods import DrawingMethods, MathematicalCalculationMethods


def initialize_video_capture():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")
    return cap


def process_frame(frame, width, height, newCircles):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20,
                              param1=70, param2=35, minRadius=5, maxRadius=100)

    countCircles = 0
    if circles is not None:
        countCircles, _ = DrawingMethods.DrawCircle(frame, circles)

    canny = cv.Canny(gray, 50, 200, None, 3)
    lines = cv.HoughLinesP(canny, rho=1, theta=np.pi / 180,
                           threshold=None, minLineLength=50, maxLineGap=10)

    process_lines_and_circles(lines, frame, width, height, newCircles)

    return countCircles, lines is not None


def process_lines_and_circles(lines, frame, width, height, newCircles):
    if lines is None:
        return

    for line in lines:
        x1, y1, x2, y2 = line[0]

    try:
        simlines = MathematicalCalculationMethods.findSimilarLines(lines, 2)
        if len(simlines) > 0:
            simLine = x1, y1, x2, y2
            x1, y1, x2, y2 = MathematicalCalculationMethods.averageLineReturnsLine(simlines)
            k, b = MathematicalCalculationMethods.getLineEquation(x1, y1, x2, y2)
            x1 = 0
            y1 = int(k * x1 + b)
            x2 = width
            y2 = int(k * x2 + b)
            avgLine = x1, y1, x2, y2

            P1 = np.array([x1, y1])
            P2 = np.array([x2, y2])
            pointsOfLine = MathematicalCalculationMethods.createLineIterator(P1, P2, height, width)
            numberOfCrossings = 0
            arrayPointsOfLine = np.ndarray.tolist(pointsOfLine)

            if MathematicalCalculationMethods.needToReverse(arrayPointsOfLine, height, frame):
                pointsOfLine = sorted(pointsOfLine, key=lambda x: x[0], reverse=True)

            isFoundSecondCrossing = False
            isFoundFirstCrossing = False

            for point in pointsOfLine:
                if not isFoundSecondCrossing:
                    b, g, r = frame[point[1], point[0]]
                    if g > 200 and r < 100 and b < 100:
                        numberOfCrossings += 1
                        if numberOfCrossings > 0 and not isFoundFirstCrossing:
                            minDist = 99999999
                            for (x, y, r) in newCircles:
                                distance = int(math.sqrt(abs((point[0] - x) ** 2) + abs((point[1] - y) ** 2)))
                                if distance < minDist:
                                    minDist = distance
                                    minCircleX = int(x)
                                    minCircleY = int(y)
                                    minCircleR = int(r)
                            newCircles.remove([minCircleX, minCircleY, minCircleR])
                            cv.circle(frame, (minCircleX, minCircleY), 40, (0, 0, 255), 2)
                            isFoundFirstCrossing = True

                        if numberOfCrossings > 0:
                            x1, y1 = point[0], point[1]
                            for (x2, y2, r) in newCircles:
                                if not isFoundSecondCrossing:
                                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                                    if abs(distance - 2 * r) < 2 * r / 20:
                                        cv.circle(frame, (x1, y1), int(r), (0, 0, 255), 2)
                                        DrawingMethods.DrawRay(frame, x1, y1, x2, y2, 100)
                                        isFoundSecondCrossing = True
                                        break
                cv.line(frame, (point[0], point[1]), (point[0], point[1]), (255, 0, 0), 1)

    except Exception as ex:
        print(traceback.format_exc())
        print(ex)


def main():
    cap = initialize_video_capture()

    start_time = time.time()
    frame_count = 0
    countCircles = 0
    countLines = 0
    newCircles = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        countCircles, line_detected = process_frame(frame, width, height, newCircles)

        cv.imshow("Camera", frame)
        frame_count += 1
        handle_fps_and_output(start_time, frame_count, countCircles, countLines)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def handle_fps_and_output(start_time, frame_count, countCircles, countLines):
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1.0:
        fps = frame_count / elapsed_time
        print(f"Frames per second: {fps:.2f}", "number of circles:", countCircles, "number of lines:", countLines)
        frame_count = 0
        start_time = time.time()


if __name__ == "__main__":
    main()
