import cv2 
import numpy as np
MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080

def in_lines(x1, x2, y1, y2, lines, threshold=30):
    for line in lines:
        start_point = line[0]
        end_point = line[1]
        y = int((y1 + y2)/2)
        if y < start_point[1] + threshold and y > start_point[1] - threshold:
            return True
            
    return False

def crossing_middle_X(x1, x2, middle_x, threshold=5):
    middle_point = int((x1 + x2)/2) 
    if middle_point >= middle_point - threshold and middle_point <= middle_x +threshold:
        return True
    return False

def get_ices(image, w_image, h_image):
    img = image.copy()
    rel_x = 200 / MAX_WINDOW_WIDTH
    rel_y = 25 / MAX_WINDOW_HEIGHT
    rel_w = 130 / MAX_WINDOW_WIDTH
    rel_minLineLength = 50/ MAX_WINDOW_WIDTH
    x = int(rel_x * w_image)
    y = int(rel_y * h_image)
    w = int(rel_w * w_image)
    minLineLength = int(rel_minLineLength * w_image)
    img = img[:img.shape[0]-y, x:x+w]
    img = cv2.GaussianBlur(img, (3,3), 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    horizontal_kernel = np.array([[1, 1, 1, 1, 1]], dtype=np.uint8)
    horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
    lines = cv2.HoughLinesP(horizontal_lines, 1, np.pi / 180, threshold=50, minLineLength=minLineLength, maxLineGap=10)
    wanted_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x1 += x
            x2 += x
            # y1 -=y
            # y2 -=y
            h = abs(y1 - y2)
            if h > 2:
                continue
            middle_x = int(image.shape[1]/2)
            if not crossing_middle_X(x1, x2, middle_x, 10):
                continue
            if not in_lines(x1, x2, y1, y2, wanted_lines, 100):
                wanted_lines.append([[x1, y1], [x2, y2]])
    return wanted_lines
