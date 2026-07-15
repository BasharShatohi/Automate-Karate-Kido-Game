from start_up_loops import play_button_loop, start_window_loop
from game_loop import game_loop
def main_loop():
    print('code_start')
    play_button_loop()
    start_window_loop()
    game_loop()

main_loop()