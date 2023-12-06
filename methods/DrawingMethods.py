import cv2
import numpy as np

def draw_circle(image, circles):
    """
    Draws circles on the given image.

    Parameters:
    - image (numpy.ndarray): The input image on which circles will be drawn.
    - circles (numpy.ndarray): A 2D array containing circle parameters (x, y, r).

    Returns:
    - count_circles (int): The number of circles drawn.
    - new_circles (list): A list of circles drawn, each represented by a 3-element list [x, y, r].
    """
    
    # Convert circle parameters to integer values
    circles = np.round(circles[0, :]).astype("int")
    new_circles = []

    try:
        if circles is not None:
            # Loop over the circles
            for (x, y, r) in circles:
                new_circles.append([x, y, r])
                # Draw the circle in the output image
                cv2.circle(image, (x, y), r, (0, 255, 0), 1)
                # Draw the circle center in the output image
                cv2.circle(image, (x, y), 0, (0, 0, 255), 2)
            
            count_circles = len(circles)
            return count_circles, new_circles
    except TypeError:
        pass


def draw_lines(image, lines):
    """
    Draws lines on the given image.

    Parameters:
    - image (numpy.ndarray): The input image on which lines will be drawn.
    - lines (numpy.ndarray): A 2D array containing line parameters (x1, y1, x2, y2).

    Returns:
    - count_lines (int): The number of lines drawn.
    """
    
    # Check if lines are detected
    if lines is not None:
        # Iterate over the array of lines
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Draw the line on the image
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        count_lines = len(lines)
        return count_lines


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

def draw_line(image, line):
    """
    Draws a single line on the given image.

    Parameters:
    - image (numpy.ndarray): The input image on which the line will be drawn.
    - line (tuple): A tuple containing line parameters (x1, y1, x2, y2).

    Returns:
    None
    """
    
    x1, y1, x2, y2 = line
    # Draw the line on the image
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)


def draw_ray(image, x1, y1, x2, y2, length):
    """
    Draws a ray on the given image starting from (x1, y1) in the direction of (x2, y2) with the specified length.

    Parameters:
    - image (numpy.ndarray): The input image on which the ray will be drawn.
    - x1, y1 (int): Starting coordinates of the ray.
    - x2, y2 (int): Directional coordinates used to determine the direction of the ray.
    - length (int): Length of the ray.

    Returns:
    None
    """
    
    # Calculate the direction vector
    direction = (x2 - x1, y2 - y1)

    # Compute the end point of the ray
    x3, y3 = int(x1 + length * direction[0]), int(y1 + length * direction[1])

    # Draw the line from the starting point to the end point
    cv2.line(image, (x1, y1), (x3, y3), (255, 0, 0), thickness=2, lineType=cv2.LINE_AA)