from pywinauto.application import Application
import mss
import cv2 as cv
import numpy as np
import os
import time
import argparse
from pynput import keyboard as pynput_keyboard
from pynput import mouse as pynput_mouse
import threading


def get_monitor(game, partial_percent=0.1):

    rect = game.rectangle()
    width_trim = int(rect.width() * partial_percent)
    height_trim = int(rect.height() * partial_percent)
    pp = (1 - (partial_percent * 2))
    monitor = {
        "top": rect.top + height_trim,
        "left": rect.left + width_trim,
        "width": int(rect.width() * pp),
        "height": int(rect.height() * pp),
    }
    return monitor


def main():
    # Directory to save screenshots
    SAVE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "images")
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Capture a window on a hotkey press.")
    parser.add_argument("--hotkey", type=str, default='l',
                        help="Key to trigger screenshot (keyboard key or mouse side button: x1, x2)")
    parser.add_argument("--app_title", type=str, default="Where Winds Meet",
                        help="Window title of the application (default: 'Where Winds Meet')")
    args = parser.parse_args()
    hotkey = args.hotkey.lower()
    APP_TITLE = args.app_title

    # Connect to the app window
    try:
        app = Application().connect(title=APP_TITLE, found_index=0)
        game = app[APP_TITLE]
        print(f"Connected to '{APP_TITLE}' window.")
    except Exception as e:
        print(f"Could not find window '{APP_TITLE}': {e}")
        return

    monitor = get_monitor(game, partial_percent=0.1)

    # Capture function
    def capture():
        with mss.mss() as sct:

            img = np.array(sct.grab(monitor))
            img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            filename = os.path.join(
                SAVE_DIR, f"screenshot_{int(time.time())}.png")
            cv.imwrite(filename, img)
            print(f"Saved {filename}")

    # Event for clean exit
    exit_event = threading.Event()

    # Mouse buttons mapping
    mouse_buttons = {'x1': pynput_mouse.Button.x1,
                     'x2': pynput_mouse.Button.x2}

    # Start listener depending on hotkey type
    if hotkey in mouse_buttons:
        print(f"Hotkey set to side mouse button: {hotkey.upper()}")

        def on_click(x, y, button, pressed):
            if pressed and button == mouse_buttons[hotkey]:
                capture()

        listener = pynput_mouse.Listener(on_click=on_click)
    else:
        print(f"Hotkey set to keyboard key: {hotkey}")

        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char == hotkey:
                    capture()
            except AttributeError:
                # handle special keys like space
                if str(key).lower() == f"'{hotkey}'":
                    capture()

        listener = pynput_keyboard.Listener(on_press=on_press)

    # Start listener in a separate thread
    listener.start()
    print(
        f"Press '{hotkey}' to capture the window '{APP_TITLE}'. Press Ctrl+C to exit.")

    try:
        while not exit_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        listener.stop()
        exit_event.set()


if __name__ == "__main__":
    main()
