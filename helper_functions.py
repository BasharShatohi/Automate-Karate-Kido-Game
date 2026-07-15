
import cv2
import numpy as np
import time
import keyboard
import pyautogui
import datetime

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
        print('press left or right arrows')
        return pt

MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080

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

def game_event(image):
    # if is_play_button_screen(image):
    #     return 'lost'  
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

def get_new_actions(actions):
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

