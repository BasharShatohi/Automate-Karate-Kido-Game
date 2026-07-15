import cv2
import numpy as np
import time
import keyboard
import pyautogui
import datetime

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
    print(thresholds)
    index = 0
    maxx = 0
    for i in range(len(thresholds)):
        if thresholds[i] > maxx:
            index = i
            maxx = thresholds[i]
    return [matches[index]]

def in_rectangles(x, y, w, h, rectangles, x_threshold, y_threshold, w_image, h_image):
    rel_x_threshold = x_threshold / MAX_WINDOW_WIDTH
    rel_y_threshold = y_threshold / MAX_WINDOW_HEIGHT
    x_threshold=int(rel_x_threshold * w_image)
    y_threshold=int(rel_y_threshold * h_image)
    for rectangle in rectangles:
        top = rectangle[0]
        bottom = rectangle[1]
        if x < top[0] + x_threshold and x > top[0] - x_threshold:
            if y < top[1] + y_threshold and y > top[1] - y_threshold:
                return True
    return False

def in_tree(image, top, buttom, w_image, h_image):
    rel_x = 180 / MAX_WINDOW_WIDTH
    rel_w = 160 / MAX_WINDOW_WIDTH
    x, w = int(rel_x * w_image), int(rel_w * w_image)
    # x, w = 170, 170
    middle_point_x = int((top[0] + buttom[0])/2)
    main_middle_x = (x + x + w) / 2
    if  middle_point_x > main_middle_x - w/4 and middle_point_x < main_middle_x + w/4:
        return False
    
    if top[0] > x and top[0] < x + w:
        return True
    if buttom[0] > x and buttom[0] < x + w:
        return True
    
    return False
def in_tree_circle(image, point, w_image, h_image):
    rel_x = 160 / MAX_WINDOW_WIDTH
    rel_w = 200 / MAX_WINDOW_WIDTH
    x, w = int(rel_x * w_image), int(rel_w * w_image)
    # x, w = 170, 170
    main_middle_x = (x + x + w) / 2
    if  point[0] > main_middle_x - w/4 and point[0] < main_middle_x + w/4:
        return True
    
    return False


def get_branches_rectangles(image, w_image, h_image):
    # in this code R is B and B is R
    
    lower_B, lower_G, lower_R = 208, 130, 82
    upper_B, upper_G, upper_R = 213, 140, 88
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask1 = cv2.inRange(image, lower_bound, upper_bound)
    
    lower_B, lower_G, lower_R = 138, 58, 28
    upper_B, upper_G, upper_R = 142, 64, 32
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask2 = cv2.inRange(image, lower_bound, upper_bound)
    
    # lower_B, lower_G, lower_R = 169, 149, 170
    # upper_B, upper_G, upper_R = 171, 151, 172
    
    # lower_bound = np.array([lower_R, lower_G, lower_B])
    # upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask3 = cv2.inRange(image, lower_bound, upper_bound)
    # rgb(97, 73, 85)
    lower_B, lower_G, lower_R = 97, 72, 84
    upper_B, upper_G, upper_R = 97, 74, 85
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask4 = cv2.inRange(image, lower_bound, upper_bound)
    
    # rgb(135, 97, 77)
    lower_B, lower_G, lower_R = 134, 96, 76
    upper_B, upper_G, upper_R = 136, 98, 79
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask5 = cv2.inRange(image, lower_bound, upper_bound)
    
    # rgb(132, 141, 164)
    lower_B, lower_G, lower_R = 130, 140, 160
    upper_B, upper_G, upper_R = 136, 145, 165
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask6 = cv2.inRange(image, lower_bound, upper_bound)
    
    # lower_B, lower_G, lower_R = 210, 178, 151
    # upper_B, upper_G, upper_R = 212, 180, 152
    
    # lower_bound = np.array([lower_R, lower_G, lower_B])
    # upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask7 = cv2.inRange(image, lower_bound, upper_bound)
    
    lower_B, lower_G, lower_R = 218, 162, 132
    upper_B, upper_G, upper_R = 220, 165, 138
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask8 = cv2.inRange(image, lower_bound, upper_bound)

    lower_B, lower_G, lower_R = 208, 177, 152
    upper_B, upper_G, upper_R = 210, 180, 155
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask9 = cv2.inRange(image, lower_bound, upper_bound)
    
    lower_B, lower_G, lower_R = 220, 173, 142
    upper_B, upper_G, upper_R = 222, 175, 145
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask10 = cv2.inRange(image, lower_bound, upper_bound)
    

    num_colored_pixels = cv2.countNonZero(mask1)
    
    masks = mask1 + mask2 + mask3 + mask4 + mask5 + mask6 + mask7 + mask8 + mask9 + mask10
    contours, _ = cv2.findContours(masks, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangles = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 4 and h > 4 and x not in range(int(image.shape[1]/2 - 50), int(image.shape[1]/2 + 40) + 1):
            if in_rectangles(x, y, w, h, rectangles, 30, 30, w_image, h_image):
                continue
            rectangles.append([[x, y], [x + w, y + h]])
    return rectangles

    
def get_orb_templates(image, xs, threshold=0.5):
    matches = []
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect keypoints and compute descriptors for the image
    orb = cv2.ORB_create()
    kp_img, des_img = orb.detectAndCompute(img, None)
    
    for x in xs:
        template = x[0]
        kp_temp, des_temp = orb.detectAndCompute(template, None)
        
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches_temp = bf.match(des_temp, des_img)
        matches_temp = sorted(matches_temp, key=lambda x: x.distance)
        
        # Apply threshold to filter matches
        filtered_matches = [m for m in matches_temp if m.distance < threshold]
        
        if len(filtered_matches) > 0:
            # Get the first match (assuming we want the best match)
            match = filtered_matches[0]
            
            # Calculate the ratio of the sum of distances between keypoints
            ratio = match.distance / threshold
            
            # Check if the ratio meets our criteria
            if ratio > threshold:
                src_pts = np.float32([kp_temp[m.queryIdx].pt for m in filtered_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp_img[m.trainIdx].pt for m in filtered_matches]).reshape(-1, 1, 2)
                
                M, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts, cv2.RANSAC, 100)
                
                # Transform the template coordinates using the affine transformation matrix
                transformed_coords = cv2.perspectiveTransform(np.float32([[0, 0], [template.shape[1]-1, 0], [template.shape[1]-1, template.shape[0]-1]]), M)
                
                # Get the bounding box of the matched region in the original image
                x, y, w, h = cv2.boundingRect(transformed_coords)
                
                # Calculate the top-left and bottom-right coordinates of the matched region
                top_left = (int(x), int(y))
                bottom_right = (int(x + w), int(y + h))
                
                matches.append([x, [top_left, bottom_right]])
    
    return matches


def get_match_templates(image, xs, threshold = 0.7):
    matches = []
    img = image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
    print('matches', matches)
    if len(matches) > 0:
        return [matches[-1]]
    return None

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

def in_section(image, start_y, end_y, branches, numbers, ice_lines):
    action  = ''
    for branch in branches: 
        top = branch[0]
        bottom = branch[1]
        middle_x = int((top[0] + bottom[0])/2)
        middle_y = int((top[1] + bottom[1])/2)
        if middle_y > start_y and middle_y < end_y:
            if middle_x < image.shape[1]/2:
                action = 'right'
            elif middle_x > image.shape[1]/2:
                action = 'left'
            break
    number_of_hits = 1
    for number in numbers:
        num, line = number
        pt1, pt2 = line
        if pt1[1] >  start_y and pt2[1] < end_y:
            number_of_hits += num - 1 
            break
    for ice_line in ice_lines:
        pt1, pt2 = ice_line
        if pt1[1] >  start_y  and pt2[1] < end_y:
            number_of_hits += 1
            break
    return 'wait' if action == '' else action, number_of_hits

def screen_taker():
    import datetime
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # screenshot.save(f"folder2/screenshot_{timestamp}.png")
    
    opencv_image = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    return opencv_image

def check_for_missing_branches(image, branches, w_image, h_image):
    x1 = cv2.imread('left_ice_brench.png', 0)
    x2 = cv2.imread('right_ice_brench.png', 0)
    xs = [[x1, 1], [x2,2]]
    matches =  get_match_templates(image, xs, 0.7)
    print('matches', matches)
    for num, match in matches:
        addition = 0
        if num == 1:
            addition =  0
        else:
            addition = 30
        top = match[0]
        bottom = match[1]
        top = [top[0]+ addition, top[1]]
        bottom = [bottom[0]+ addition, bottom[1]]
        if not in_rectangles(top[0], top[1], (bottom[0] - top[0]), (bottom[1] - top[1]), branches, 50, 50, w_image, h_image):
            branches.append([top, bottom])
    return branches

def game_event(image):
    rel_x = 600 / MAX_WINDOW_WIDTH
    rel_y = 300 / MAX_WINDOW_HEIGHT
    rel_w = 700 / MAX_WINDOW_WIDTH
    rel_h = 600 / MAX_WINDOW_HEIGHT
    rel_end_game_y = 350/MAX_WINDOW_HEIGHT
    rel_game_uplevel_y = 550/MAX_WINDOW_HEIGHT
    rel_threshold = 50/MAX_WINDOW_HEIGHT 
    h_image, w_image, _ = image.shape
    x = int(rel_x * w_image)
    y = int(rel_y * h_image)
    w = int(rel_w * w_image)
    h = int(rel_h * h_image)
    end_game_y = int(rel_end_game_y * h_image)
    game_uplevel_y = int(rel_game_uplevel_y * h_image)
    threshold = int(rel_threshold * h_image)

    image = image[y:y+h, x:x+w]
    max_line = int(image.shape[1]/2)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=max_line, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1-y2) <=10:
                if y1 > end_game_y - threshold and y1 < end_game_y + threshold: 
                    return 'lost'
                    
                elif y1 > game_uplevel_y - threshold and y1 < game_uplevel_y + threshold:
                    return 'uplevel'

    return ''

def get_new_actions(actions):
    # beta_action = []
    # i = 0
    # while i < len(actions):
    #     if i < len(actions) - 1 and ((actions[i][0] == 'right' and actions[i+1][0] == 'left') or (actions[i][0] == 'left' and actions[i+1][0] == 'right')):
    #         beta_action.append((actions[i+1][0], actions[i][1]))
    #         beta_action.append((actions[i+1][0], actions[i+1][1]))
    #         i+=2
    #         continue
    #     beta_action.append((actions[i][0], actions[i][1]))
    #     i+=1
    # print(beta_action)
    beta_action = actions.copy()
    new_actions = []
    for i in range(len(beta_action)):
        if beta_action[i][0] != 'wait':
            new_actions.append(beta_action[i])
            continue
        for index in range(i + 1, len(beta_action)):
            if beta_action[index][0] != 'wait':
                new_actions.append((beta_action[index][0], beta_action[i][1]))
                break
    return new_actions

def kick(action, kick_nums, middle_point):
    pp = ''
    for i in range(kick_nums):
        if action == 'left':
            pyautogui.click(button='left', x=middle_point[0] - 200, y=middle_point[1])
            
            pp = 'left'
        elif action == 'right':
            pyautogui.click(button='left', x=middle_point[0] + 200, y=middle_point[1])
            
            pp = 'right'
    return  pp

def match_template(main_image, template):
    gray_main = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = gray_template.shape[::-1]
    result = cv2.matchTemplate(gray_main, gray_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8 
    loc = np.where(result >= threshold)

    if loc[0].size > 0 and loc[1].size > 0: 
        for pt in zip(*loc[::-1]): 
            cv2.rectangle(main_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2) 
            return pt
    else: 
        return None

def is_play_button_screen(image):
    template = cv2.imread('play_button.jpg')
    pt = match_template(image, template)
    if pt:
        print('button found')
        return pt
        
def is_start_window_screen(image):
    template = cv2.imread('windows_start.jpg')
    pt = match_template(image, template)
    if pt:
        print('press left or right arrows')
        return pt

def play_button_loop():
    on_play_screen = True
    while on_play_screen:
        image = screen_taker()
        pt = is_play_button_screen(image)
        if pt:
            pyautogui.mouseDown(int(pt[0]+10), int(pt[1]+10))
            time.sleep(0.5)
            pyautogui.mouseUp()
            on_play_screen = False

def start_window_loop():
    on_start_screen = True
    while on_start_screen:
        image = screen_taker()
        pt = is_start_window_screen(image)
        if pt:
            pyautogui.mouseDown(int(pt[0]+10), int(pt[1]+10))
            pyautogui.mouseUp()
            on_start_screen = False
            return

def game_loop():
    position = 'right'
    change_player = True
    main_start_y = 470
    main_end_y = 570
    section_threshold = 95
    while True:
        screen_image = screen_taker()
        image = screen_image.copy()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        cv2.imwrite(f"folder2/screenshot_{timestamp}.png", image)
        rel_x = 700 / MAX_WINDOW_WIDTH
        rel_y = 300 / MAX_WINDOW_HEIGHT
        rel_w = 500 / MAX_WINDOW_WIDTH
        rel_h = 580 / MAX_WINDOW_HEIGHT
        h_image, w_image, _ = image.shape
        x = int(rel_x * w_image)
        y = int(rel_y * h_image)
        w = int(rel_w * w_image)
        h = int(rel_h * h_image)
        if change_player:    
            value = get_players(image)
            # print(value)
            if value is None or len(value) == 0:
                continue
            player_type = value[0][0]
            print(player_type)
            change_player = False
        if player_type == 1:
            # player = 450
            rel_section_threshold = 100 / MAX_WINDOW_HEIGHT
            rel_main_start_y = 470 / MAX_WINDOW_HEIGHT
            rel_main_end_y = 570 / MAX_WINDOW_HEIGHT
            section_threshold = int(rel_section_threshold * h_image) 
            main_end_y = int(rel_main_end_y * h_image) 
            main_start_y = int(rel_main_start_y * h_image)
        elif player_type == 2:
            rel_section_threshold = 100 / MAX_WINDOW_HEIGHT
            rel_main_start_y = 448 / MAX_WINDOW_HEIGHT
            rel_main_end_y = 558 / MAX_WINDOW_HEIGHT
            section_threshold = int(rel_section_threshold * h_image) 
            main_end_y = int(rel_main_end_y * h_image) 
            main_start_y = int(rel_main_start_y * h_image)
        elif player_type ==3:
            rel_section_threshold = 120 / MAX_WINDOW_HEIGHT
            rel_main_start_y = 428 / MAX_WINDOW_HEIGHT
            rel_main_end_y = 538 / MAX_WINDOW_HEIGHT
            section_threshold = int(rel_section_threshold * h_image) 
            main_end_y = int(rel_main_end_y * h_image) 
            main_start_y = int(rel_main_start_y * h_image)
    
        image = image[y:y+h, x:x+w]
        
        g_event = game_event(image)
        if g_event == 'uplevel':
            print(g_event)
            time.sleep(8)
            change_player = True
        elif g_event == 'lost':
            print(g_event)
            break

        numbers = get_numbers(image)
        powers = get_powers(image, w_image, h_image)
        ice_lines = get_ices(image, w_image, h_image)
        branches = get_branches_rectangles(image, w_image, h_image)
        # if len(ice_lines) > 0:
        #     branches = check_for_missing_branches(image, branches, w_image, h_image)
        player_position = 'right'
        
        start_y = main_start_y
        end_y = main_end_y
        actions = []
        counter = 0
        for i in range(3): 
            action = in_section(image, start_y, end_y, branches, numbers, ice_lines)
            actions.append(action)
            end_y = start_y
            start_y -= section_threshold
            counter = 3
            if i == 2 and actions[len(actions) - 1][0] == 'wait':
                counter = 4
                action = in_section(image, start_y, end_y, branches, numbers, ice_lines)
                actions.append(action)
        if powers:
            start_y = main_start_y
            end_y = main_end_y
            for i in range(counter):
                power = powers[0]
                point = power[1]
                y = point[0][1]
                if y > start_y and y < end_y:
                    if i == counter - 1 or i == 0 or actions[i-1][0]!='wait' and actions[i][0]!='wait':
                        break
                    
                    # new_actions = [] 
                    this_action = actions[i+1][0]
                    if this_action == 'left':
                        this_action = 'right'
                    else:
                        this_action = 'left'
                    actions[i-1] = (this_action, actions[i-1][1])
                    actions[i] = (actions[i+1][0], actions[i][1])
                    # actions = new_actions.copy()
                    break 
                end_y = start_y
                start_y -= section_threshold
        actions = get_new_actions(actions)
        
        print(actions)
        middle_point = [w_image // 2, h_image // 2]
        for action in actions:
            player_position = kick(action[0], action[1], middle_point)
        time.sleep(0.3)
        

def game_test():
    player_type = 2
    position = 'right'
    change_player = True
    main_start_y = 470
    main_end_y = 570
    section_threshold = 95
    # screen_image = cv2.imread('folder2/screenshot_2025-01-06_15-57-01.png')
    # screen_image = cv2.imread('folder2/screenshot_2025-01-07_11-55-56.png')
    # screen_image = cv2.imread('folder2/screenshot_2025-01-07_12-59-23.png')
    
    screen_image = cv2.imread('folder/screenshot_2025-01-09_11-53-23.png')
    # screen_image = cv2.imread('folder/screenshot_2025-01-09_11-21-01.png')
    # screen_image = cv2.imread('folder/screenshot_2025-01-09_11-21-01.png')
    # player_type = get_players(screen_image)
    # screen_image = cv2.imread('folder2/screenshot_2025-01-07_12-59-23.png')
    image = screen_image.copy()
    print(game_event(screen_image))
    value = get_players(screen_image)
    print('value', value)
    if value is None or len(value) == 0:
        return
    
    player_type = value[0][0]
    print(player_type)
    rel_x = 700 / MAX_WINDOW_WIDTH
    rel_y = 300 / MAX_WINDOW_HEIGHT
    rel_w = 500 / MAX_WINDOW_WIDTH
    rel_h = 580 / MAX_WINDOW_HEIGHT
    h_image, w_image, _ = image.shape
    x = int(rel_x * w_image)
    y = int(rel_y * h_image)
    w = int(rel_w * w_image)
    h = int(rel_h * h_image)
    # print(player_type)

    if player_type == 1:
        # player = 450
        rel_section_threshold = 100 / MAX_WINDOW_HEIGHT
        rel_main_start_y = 465 / MAX_WINDOW_HEIGHT
        rel_main_end_y = 565 / MAX_WINDOW_HEIGHT
        section_threshold = int(rel_section_threshold * h_image) 
        main_end_y = int(rel_main_end_y * h_image) 
        main_start_y = int(rel_main_start_y * h_image)
    elif player_type == 2:
        rel_section_threshold = 100 / MAX_WINDOW_HEIGHT
        rel_main_start_y = 448 / MAX_WINDOW_HEIGHT
        rel_main_end_y = 558 / MAX_WINDOW_HEIGHT
        section_threshold = int(rel_section_threshold * h_image) 
        main_end_y = int(rel_main_end_y * h_image) 
        main_start_y = int(rel_main_start_y * h_image)
    elif player_type ==3:
        rel_section_threshold = 120 / MAX_WINDOW_HEIGHT
        rel_main_start_y = 428 / MAX_WINDOW_HEIGHT
        rel_main_end_y = 538 / MAX_WINDOW_HEIGHT
        section_threshold = int(rel_section_threshold * h_image) 
        main_end_y = int(rel_main_end_y * h_image) 
        main_start_y = int(rel_main_start_y * h_image)

    image = image[y:y+h, x:x+w]
    if change_player:    
        player_type = get_players(screen_image)
        change_player = False

    g_event = game_event(image)
    if g_event == 'uplevel':
        change_player = False
    elif g_event == 'lost':
        print('you lost')
        
    # print(branches)
    numbers = get_numbers(image)
    powers = get_powers(image, w_image, h_image)
    ice_lines = get_ices(image, w_image, h_image)
    branches = get_branches_rectangles(image, w_image, h_image)
    # if len(ice_lines) > 0: 
    #     branches = check_for_missing_branches(image, branches, w_image, h_image)
    player_position = 'right'
    
    start_y = main_start_y
    end_y = main_end_y
    actions = []
    counter = 0
    for i in range(4): 
        action = in_section(image, start_y, end_y, branches, numbers, ice_lines)
        cv2.rectangle(image, (10, start_y), (400, end_y), 100, 3)
        actions.append(action)
        end_y = start_y
        start_y -= section_threshold
        counter = 3
        if i == 2 and actions[len(actions) - 1][0] == 'wait':
            counter = 4
            action = in_section(image, start_y, end_y, branches, numbers, ice_lines)
            actions.append(action)
    print(actions)
    if powers:
        start_y = main_start_y
        end_y = main_end_y
        for i in range(counter):
            power = powers[0]
            point = power[1]
            y = point[0][1]
            if y > start_y and y < end_y:
                if i == counter - 1 or i == 0 or actions[i-1][0]!='wait':
                    break
                
                # new_actions = [] 
                this_action = actions[i+1][0]
                if this_action == 'left':
                    this_action = 'right'
                else:
                    this_action = 'left'
                actions[i-1] = (this_action, actions[i-1][1])
                actions[i] = (actions[i+1][0], actions[i][1])
                # actions = new_actions.copy()
                break 
            end_y = start_y
            start_y -= section_threshold
    for branch in branches:
        cv2.rectangle(image, branch[0], branch[1], 255, 3)
    # print(ice_lines)
    for ice in ice_lines:
        cv2.line(image, ice[0], ice[1], 255, 3)
    for power in powers:
        # print(power)
        num, p = power
        point, r = p 
        # print(point, r)
        cv2.circle(image, point, r, 255, 3)
    actions = get_new_actions(actions)
    print(actions)
    cv2.imshow('image', image)
    cv2.waitKey()

def main_loop():
    print('code_start')
    play_button_loop()
    start_window_loop()
    game_loop()

game_test()