import pynput
from pynput import mouse, keyboard
import threading
import time
import pyautogui

class MousePositionRecorder:
    def __init__(self):
        self.positions = []
        self.mouse_listener = None
        self.keyboard_listener = None
        self.running = True
        
    def get_mouse_position(self):
        """Get current mouse position"""
        return pyautogui.position()
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            if key == keyboard.Key.space:
                # Record current mouse position
                pos = self.get_mouse_position()
                self.positions.append(pos)
                print(f"Recorded position: ({pos[0]}, {pos[1]})")
                
            elif key == keyboard.Key.esc:
                # Save positions and exit
                self.save_positions()
                print("Escape pressed. Stopping recorder...")
                self.running = False
                return False  # Stop listener
                
        except AttributeError:
            # Handle special keys that don't have char attribute
            pass
    
    def save_positions(self):
        """Save recorded positions to file"""
        if not self.positions:
            print("No positions recorded.")
            return
            
        filename = f"mouse_positions_{int(time.time())}.txt"
        try:
            with open(filename, 'w') as f:
                for pos in self.positions:
                    f.write(f"({int(pos[0])}, {int(pos[1])})\n")
            print(f"Saved {len(self.positions)} positions to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")
    
    def start_recording(self):
        """Start the recording process"""
        print("Mouse Position Recorder Started")
        print("Press SPACE to record current mouse position")
        print("Press ESC to save positions and exit")
        print("-" * 40)
        
        # Start keyboard listener
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

def main():
    recorder = MousePositionRecorder()
    try:
        recorder.start_recording()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()