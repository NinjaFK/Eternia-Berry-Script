import minescript
import time
import pyautogui
import keyboard
import re
import io
from contextlib import redirect_stdout
# Write a message to the chat that only you can see:


# print(dir(minescript))
# with open("C:\\Users\\nieh_\\curseforge\\minecraft\\Instances\\Official Eternia Cobblemon\\minescript\\help.txt", "w") as f:
#     with redirect_stdout(f):
#         help(minescript)

def buy_bones():
    # Teleport to the shop
    minescript.execute(f"home shop")

    expected_shop_name = "Buy/Sell Shop"
    shop_bool = False

    t_end = time.time() + 4
    while time.time() < t_end:
        if minescript.player_get_targeted_entity() is not None:
            shop = minescript.player_get_targeted_entity()
            input_shop_name = shop.name
            if expected_shop_name == input_shop_name:
                shop_bool = True
                break


    
    if not shop_bool:
        print("Wrong shop please try again")
        return
    
    print("Shop Name: " + input_shop_name)
    print("Correct Shop\nStarting Buy bones")
    minescript.player_press_use(True)

    # with open("C:\\Users\\nieh_\\curseforge\\minecraft\\Instances\\Official Eternia Cobblemon\\minescript\\output.txt", "w") as f:
    #     f.write(name)



def move_item():
    pyautogui.click(button='right')
    pyautogui.keyDown('shiftleft')
    pyautogui.click()
    pyautogui.click()
    pyautogui.keyUp('shiftleft')
    pyautogui.click()
    pyautogui.keyDown('shiftleft')
    pyautogui.click()
    pyautogui.keyUp('shiftleft')
    pyautogui.press('esc')

    

def fill_inventory() -> bool:

    # open chest

    berries = 0
    time.sleep(.75)
    grab = 0
    for item in minescript.container_get_items():
        if item.slot > 53:
            break
        berries += item.count
        if item.count > 32:
            grab = item.slot

    
    # Move the items to inventory if enough
    if berries > 384:
        # print("Chest Has Enough")
        move_to_position(grab)
        move_item()
        return True
    else:
        pyautogui.press('esc')
        # print("Chest doesnt have Enough")
        return False



def item_to_backpack() -> bool:

    grab = 0
    berries = 0
    for item in minescript.player_inventory():
        berries += item.count
        if item.count > 32:
            grab = item.slot
    
    # if berries > 1728:
        # print("Inventory has enough")

    
    pyautogui.press('b')
    time.sleep(.1)

    berries = 0

    t_end = time.time() + 4
    while time.time() < t_end:
        if minescript.container_get_items() is not None:
            break
    for item in minescript.container_get_items():
        if item.slot > 53:
            break
        berries += item.count
    
    if berries != 3456:
        time.sleep(.3)
        move_to_position(grab + 53)
        move_item()
        return True
    else:
        pyautogui.press('esc')
        print("Full backpack")




def sell():
    time.sleep(.1)
    pyautogui.click(button='right')

    t_end = time.time() + 4
    while time.time() < t_end:
        if minescript.container_get_items() is not None:
            break

    move_to_position(40)
    pyautogui.click(button='right')
    move_to_position(19)
    for i in range(36):
        time.sleep(.1)
        pyautogui.click()
    
    move_to_position(39)
    pyautogui.click()
    time.sleep(.1)
    pyautogui.press('esc')

def sell_at_shop():

    # in case of fast command use
    time.sleep(.5)
    # Teleport to Shop
    minescript.execute(f"home berry-s")
    time.sleep(1.6)

    expected_shop_name = "Beatrice The Berry Lady"
    shop_bool = False

    t_end = time.time() + 4
    while time.time() < t_end:
        if minescript.player_get_targeted_entity() is not None:
            shop = minescript.player_get_targeted_entity()
            input_shop_name = shop.name
            if expected_shop_name == input_shop_name:
                shop_bool = True
                break

    if not shop_bool:
        print("Wrong shop please try again")
        return
    
    # print("Shop Name: " + input_shop_name)
    print("Correct Shop\nStarting Sell berries")

    sell()
    time.sleep(.4)
    pyautogui.press('b')
    time.sleep(.2)
    fill_inventory()
    time.sleep(.2)
    sell()
    time.sleep(.2)
    pyautogui.press('b')
    time.sleep(.2)
    fill_inventory()
    sell()
    
    minescript.execute(f"back")
    time.sleep(2)

    minescript.player_press_use(True)
    grab_berries()

def full() -> bool:
    time.sleep(.1)
    pyautogui.press('b')
    time.sleep(.1)

    berries = 0
    t_end = time.time() + 4
    while time.time() < t_end:
        if minescript.container_get_items() is not None:
            break
    for item in minescript.container_get_items():
        berries += item.count
    
    pyautogui.press('esc')
    
    if berries > 5697:
        return True
    else:
        return False



def grab_berries():
    for j in range(3):
            minescript.player_press_use(True)
            if not fill_inventory():
                if full():
                    print("Go to shop")
                    sell_at_shop()
                break
            if not item_to_backpack():
                if full():
                    print("Go to shop")
                    sell_at_shop()
                break



def move_right_until_next_chest():
    curr = minescript.player_get_targeted_block()
    for i in range(100):
        new = minescript.player_get_targeted_block()
        if new.type == curr.type and new.position != curr.position:
            return
        else:
            minescript.player_press_right(True)
            time.sleep(0.01)
            minescript.player_press_right(False)

def move_left_until_next_chest():
    curr = minescript.player_get_targeted_block()
    for i in range(100):
        new = minescript.player_get_targeted_block()
        if new.type == curr.type and new.position != curr.position:
            return
        else:
            minescript.player_press_left(True)
            time.sleep(0.01)
            minescript.player_press_left(False)
    

def sell_berries():
    # Teleport to the berry and look down
    minescript.execute(f"home berry")
    time.sleep(1.2)
    minescript.player_set_orientation(90.0, 90.0)


    # Wait until block is a chest
    expected_block = "minecraft:chest[facing=north,type=right,waterlogged=false]"
    chest_bool = False

    t_end = time.time() + 4
    while time.time() < t_end:
        if minescript.player_get_targeted_block() is not None:
            block = minescript.player_get_targeted_block()
            input_block = block.type
            if expected_block == input_block:
                chest_bool = True
                break
    
    if not chest_bool:
        print("Error Please Try Again")
        return
        
    for row in range(7):
        for chest in range(12):
            time.sleep(1)

            # Move to the next chest
            if row % 2 == 0:
                grab_berries()
                move_right_until_next_chest()
            else:
                grab_berries()
                move_left_until_next_chest()

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





def load_positions_from_file(filename):
    """
    Load mouse positions from a file into the global array.
    If no filename is provided, looks for the most recent mouse_positions_*.txt file.
    """
    global loaded_positions
    try:
        loaded_positions = []
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Parse (x, y) format using regex
                match = re.match(r'\((\d+),\s*(\d+)\)', line)
                if match:
                    x, y = int(match.group(1)), int(match.group(2))
                    loaded_positions.append((x, y))
                else:
                    print(f"Warning: Could not parse line {line_num}: {line}")
        
        return True
        
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False
    except Exception as e:
        print(f"Error loading positions: {e}")
        return False

def move_to_position(index):
    global loaded_positions

    x, y = loaded_positions[index]
    pyautogui.moveTo(x, y)

def main():
    load_positions_from_file("C:\\Users\\nieh_\\curseforge\\minecraft\\Instances\\Official Eternia Cobblemon\\minescript\\mouse_positions_1750826715.txt")
    sell_berries()
    # sell()

if __name__ == '__main__':
    main()

# Write a chat message that other players can see:
#minescript.chat("Hello, everyone!")

# Get your player's current position:
# x, y, z = minescript.player().position

# Print information for the block that your player is standing on:
# minescript.echo(minescript.getblock(x, y - 1, z))

# Set the block directly beneath your player (assuming commands are enabled):
# x, y, z = int(x), int(y), int(z)
# minescript.execute(f"setblock {x} {y-1} {z} yellow_concrete")

# Display the contents of your inventory:
# for item in minescript.player_inventory():
#   minescript.echo(item.item)