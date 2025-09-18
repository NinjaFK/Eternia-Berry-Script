import minescript
import time
import pyautogui
import random
import re

pyautogui.FAILSAFE = False

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
    """
    Move the mouse to the position at the specified index.
    
    Args:
        index (int): Index of the position in the loaded_positions array
        
    Returns:
        bool: True if successful, False if index is invalid
    """
    global loaded_positions
    
    if not loaded_positions:
        print("No positions loaded. Please run load_positions_from_file() first.")
        return False
    
    if index < 0 or index >= len(loaded_positions):
        print(f"Invalid index {index}. Valid range: 0-{len(loaded_positions)-1}")
        return False
    
    try:
        x, y = loaded_positions[index]
        pyautogui.moveTo(x, y)
        return True
        
    except Exception as e:
        print(f"Error moving mouse: {e}")
        return False


def get_balance() -> float:
   """
   Retrieves the current balance by executing the balance command and parsing the chat response.
   
   Returns:
       float: The balance amount as a number (e.g., 1500.0 for "$1,500.00")
   """
   while True:
       with minescript.EventQueue() as event_queue:
           event_queue.register_chat_listener()
           minescript.execute("balance")
           event = event_queue.get()
           
           # Only process chat events that contain balance information
           if event.type == minescript.EventType.CHAT and "Balance" in event.message:
               # Extract amount after '$' and remove commas
               return float(event.message.split('$')[1].replace(',', ''))


def open_buy_shop() -> bool:
    """
    Opens the buy/sell shopkeeper. Assumes the player is already looking at the correct location, likely after teleporting there

    Returns:
        boolean: Whether or not the shopkeeper was successfully opened. If this is false, break out and return an error
    """
    expected_shop_name = "Buy/Sell Shop"
    shop_bool = False

    t_end = time.time() + 5
    while time.time() < t_end:
        if minescript.player_get_targeted_entity() is not None:
            shop = minescript.player_get_targeted_entity()
            input_shop_name = shop.name
            if expected_shop_name == input_shop_name:
                shop_bool = True
                break
    
    if not shop_bool:
        print("Wrong shop please try again")
        return False
    
    minescript.player_press_use(True)
    while time.time() < t_end:
        if minescript.container_get_items() is not None:
            break
    return True


def buy_bones(num_to_buy: int, put_bones_in_backpack: bool = True) -> None:
    # Select bones
    move_to_position(21)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(1.0)
    
    move_to_position(19)
    time.sleep(0.5)
    
    # Buy a bunch of bones
    for i in range(num_to_buy):
        # Add small randomization to timing (±10ms)
        randomized_interval = (1.0 / 12) + random.uniform(-0.01, 0.01)
        pyautogui.click()
        time.sleep(randomized_interval)
    time.sleep(0.5)

    # Confirm purchace
    move_to_position(39)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

    # Exit and open bag
    pyautogui.press('escape')
    time.sleep(0.5)

    if(put_bones_in_backpack):
        pyautogui.press('b')
        time.sleep(0.5)

        # Deposit bones into bag
        move_to_position(81)
        pyautogui.click()
        time.sleep(0.25)
        move_to_position(82)
        pyautogui.keyDown("shiftleft")
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.keyUp("shiftleft")
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.keyDown("shiftleft")
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.keyUp("shiftleft")

        time.sleep(0.5)
        pyautogui.press('escape')


def fill_bone_inv():
    open_buy_shop()
    time.sleep(0.25)
    buy_bones(random.randrange(39, 44))
    time.sleep(0.25)

    open_buy_shop()
    time.sleep(0.25)
    buy_bones(random.randrange(39, 44))
    time.sleep(0.25)

    open_buy_shop()
    time.sleep(0.25)
    buy_bones(random.randrange(22, 25), False)
    time.sleep(0.25)


def get_num_bones_in_chest():
    bones = 0
    for item in minescript.container_get_items():
        if item.slot > 53:
            break
        if item.item == "minecraft:bone":
            bones += item.count
    return bones


def get_num_bones_in_inv():
    bones = 0
    for item in minescript.container_get_items():
        if item.item == "minecraft:bone" and item.slot > 53:
            bones += item.count
    return bones


def get_first_bone_in_inv():
    for item in minescript.container_get_items():
        if item.item == "minecraft:bone" and item.slot > 53:
            return item.slot
        
def get_first_bone_in_chest():
    for item in minescript.container_get_items():
        if item.item == "minecraft:bone" and item.slot < 53:
            return item.slot


def fill_chest():
    if get_num_bones_in_inv() == 0:
        return
    move_to_position(get_first_bone_in_inv())
    time.sleep(0.1)
    pyautogui.click()
    move_to_position(get_first_bone_in_inv())
    time.sleep(0.25)
    pyautogui.keyDown("shiftleft")
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.keyUp("shiftleft")
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyDown("shiftleft")
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyUp("shiftleft")

def withdraw_from_backpack():
    move_to_position(get_first_bone_in_chest())
    time.sleep(0.1)
    pyautogui.click()
    move_to_position(get_first_bone_in_chest())
    time.sleep(0.25)
    pyautogui.keyDown("shiftleft")
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.25)
    pyautogui.keyUp("shiftleft")
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyDown("shiftleft")
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyUp("shiftleft")


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
load_positions_from_file("C:\\Users\\serdr\\curseforge\\minecraft\\Instances\\Official Eternia Cobblemon\\minescript\\mouse_positions.txt")