from helpers import fill_bone_inv, get_num_bones_in_chest, get_num_bones_in_inv, fill_chest, withdraw_from_backpack, move_right_until_next_chest, move_left_until_next_chest
import minescript
import pyautogui
import time

# load_positions_from_file("mouse_positions.txt")

def main_loop():
    minescript.player_set_orientation(-90, 90)
    for row in range(6):
        chest = 0
        while chest < 12:
            # Open chest
            minescript.player_press_use(True)
            time.sleep(0.5)
            if get_num_bones_in_chest() <= 2944:
                fill_chest()

                amount_in_inv = get_num_bones_in_inv()

                pyautogui.press("esc")
                
                # If inventory is empty, withdraw from backpack
                if amount_in_inv == 0:
                    time.sleep(0.5)
                    pyautogui.press("b")
                    time.sleep(0.5)
                    
                    # If backpack is empty, go to shop
                    if get_num_bones_in_chest() <= 128:
                        pyautogui.press("esc")
                        time.sleep(0.5)

                        # Shop function
                        minescript.execute("home Sell")
                        time.sleep(1.6)
                        fill_bone_inv()
                        time.sleep(0.5)
                        
                        minescript.execute("back")
                        time.sleep(1.6)
                        
                    else:
                        withdraw_from_backpack()
                        pyautogui.press("esc")
                        time.sleep(0.5)
                    continue
            else:
                pyautogui.press("esc")
                time.sleep(0.5)


            time.sleep(1)

            # Move to the next chest
            if row % 2 == 0:
                move_right_until_next_chest()
            else:
                move_left_until_next_chest()
            
            chest += 1

        # Don't align on the last jump
        if row != 5:
            # Align with the next row
            minescript.player_press_forward(True)
            time.sleep(0.05)
            minescript.player_press_jump(True)
            if(row % 2 == 0):
                minescript.player_press_right(True)
                time.sleep(0.30)
                minescript.player_press_right(False)
            else:
                minescript.player_press_left(True)
                time.sleep(0.30)
                minescript.player_press_left(False)
            minescript.player_press_jump(False)
            time.sleep(1)
            minescript.player_press_forward(False)

time.sleep(1.5)
minescript.player_set_orientation(-90, 90)
main_loop()