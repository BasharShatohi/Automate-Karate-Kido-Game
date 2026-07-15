import cv2
import numpy as np


MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080

def get_best_match(image, xs):
    matches = []
    img = image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholds = []
    for x in xs:
        template = x[0]
        result = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        thresholds.append(max_val)
        top_left = max_loc
        h, w = template.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)
        matches.append([x[1], [top_left, bottom_right]])
    index = 0
    maxx = 0
    for i in range(len(thresholds)):
        if thresholds[i] > maxx:
            index = i
            maxx = thresholds[i]
    return [matches[index]]

def get_match_templates(image, xs, threshold = 0.7):
    matches = []
    img = image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholds = []
    for x in xs:
        template = x[0]
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            top_left = max_loc
            h, w = template.shape
            bottom_right = (top_left[0] + w, top_left[1] + h)
            matches.append([x[1], [top_left, bottom_right]])
    return matches

def get_numbers(image):
    x2 = cv2.imread('2x.png', 0)
    x3 = cv2.imread('3x.png', 0)
    x4 = cv2.imread('4x.png', 0)
    xs = [[x2, 2], [x3,3], [x4,4]]
    
    return get_match_templates(image, xs, 0.7)

def in_tree_circle(image, point, w_image, h_image):
    rel_x = 160 / MAX_WINDOW_WIDTH
    rel_w = 200 / MAX_WINDOW_WIDTH
    x, w = int(rel_x * w_image), int(rel_w * w_image)
    # x, w = 170, 170
    main_middle_x = (x + x + w) / 2
    if  point[0] > main_middle_x - w/4 and point[0] < main_middle_x + w/4:
        return True
    
    return False

def find_circles(image, w_image, h_image):
    img = image.copy()
    rel_x = 120 / MAX_WINDOW_WIDTH
    rel_w = 280 / MAX_WINDOW_WIDTH
    rel_y = 100 / MAX_WINDOW_HEIGHT
    rel_y_down = 50 / MAX_WINDOW_HEIGHT
    
    x = int(rel_x * w_image)
    w = int(rel_w * w_image)
    y = int(rel_y * h_image)
    y_down = int(rel_y_down * h_image)
    img = img[y:img.shape[1]-y_down, x:x+w]
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rel_minDist = 30 / MAX_WINDOW_WIDTH
    rel_param1 = 80 / MAX_WINDOW_WIDTH
    rel_param2 = 40 / MAX_WINDOW_WIDTH
    rel_minRadius = 20 / MAX_WINDOW_WIDTH
    rel_maxRadius = 28 / MAX_WINDOW_WIDTH
    
    minDist = int(rel_minDist * w_image)
    param1 = int(rel_param1 * w_image)
    param2 = int(rel_param2 * w_image)
    minRadius = int(rel_minRadius * w_image)
    maxRadius = int(rel_maxRadius * w_image)

    gray_blurred =  cv2.GaussianBlur(gray, (3, 3), 3)

    circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        dp=2.0,
        minDist=minDist,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius
    )
    wanted_circles = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            if not in_tree_circle(image, [i[0]+x, i[1]+y], w_image, h_image):
                wanted_circles.append([[i[0]+x, i[1]+y], i[2]])
    
    return wanted_circles


def get_powers(image, w_image, h_image):
    wanted_circles = find_circles(image, w_image, h_image) 
    results = []
    for circle in wanted_circles:
        results.append([1, circle])
    x2 = cv2.imread('power2.png', 0)
    x3 = cv2.imread('power3.png', 0)
    
    xs = [[x2, 2],[x3, 3]]
    matches = get_match_templates(image, xs, 0.6)
    for match in matches:
        _, rectangle = match
        tl = rectangle[0]
        br = rectangle[1]
        w, h = br[0]-tl[0], br[1]-tl[1] 
        circle = [[int(tl[0]+w//2), int(tl[1]+h//2)], max(w, h)//2] 
        results.append([2, circle])
    return results

def get_players(image):
    x1 = cv2.imread('player1_right.png', 0)
    x2 = cv2.imread('player1_left.png', 0)
    
    x3 = cv2.imread('player2_right.png', 0)
    x4 = cv2.imread('player2_left.png', 0)
    x5 = cv2.imread('player3_right.png', 0)
    x6 = cv2.imread('player3_left.png', 0)
    xs = [[x1, 1], [x2, 1], [x3,2], [x4, 2], [x5, 3], [x6, 3]]
    matches =  get_best_match(image, xs)
    if len(matches) > 0:
        return [matches[-1]]
    return None
