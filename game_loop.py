import cv2 
import numpy as np
import datetime
import time
from helper_functions import screen_taker
from helper_functions import in_section, game_event, get_new_actions, kick
from find_branches import get_branches_rectangles
from find_ices import get_ices
from find_objects import get_powers, get_numbers, get_players


MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080


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
        cv2.imwrite(f"folder/screenshot_{timestamp}.png", image)
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
        
        g_event = game_event(screen_image)
        if g_event == 'uplevel':
            print(g_event)
            time.sleep(5)
            change_player = True
            continue
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
                    if i == counter - 1 or i == 0 or actions[i-1][0]!='wait' or actions[i][0]!='wait':
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
        time.sleep(0.35)
        
