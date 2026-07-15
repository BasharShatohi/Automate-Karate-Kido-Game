import cv2 
import numpy as np

MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080

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
    
    lower_B, lower_G, lower_R = 169, 149, 170
    upper_B, upper_G, upper_R = 171, 151, 172
    
    lower_bound = np.array([lower_R, lower_G, lower_B])
    upper_bound = np.array([upper_R, upper_G, upper_B])
    
    mask3 = cv2.inRange(image, lower_bound, upper_bound)
    # rgb(97, 73, 85)
    lower_B, lower_G, lower_R = 97, 72, 84
    upper_B, upper_G, upper_R = 98, 74, 86
    
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
    
    # lower_B, lower_G, lower_R = 210, 176, 150
    # upper_B, upper_G, upper_R = 212, 180, 153
    
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
