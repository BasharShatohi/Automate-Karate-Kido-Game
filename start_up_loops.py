import cv2
import numpy as np
import time
import keyboard
import pyautogui
import datetime
from helper_functions import screen_taker

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

