from pywinauto.application import Application
import mss
import cv2 as cv
import numpy as np
import os
import time
import keyboard
import argparse


def main():
    # Directory to save screenshots
    SAVE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "images")
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Capture a window on a hotkey press.")
    parser.add_argument("--hotkey", type=str, default='p',
                        help="Key to trigger screenshot (e.g., `, f, space)")
    parser.add_argument("--app_title", type=str, default="Where Winds Meet",
                        help="Window title of the application (default: 'Where Winds Meet')")
    args = parser.parse_args()
    hotkey = args.hotkey
    APP_TITLE = args.app_title

    # Connect to the app window
    try:
        app = Application().connect(title=APP_TITLE, found_index=0)
        game = app[APP_TITLE]
        rect = game.rectangle()
        print(f"Connected to '{APP_TITLE}' window.")
    except Exception as e:
        print(f"Could not find window '{APP_TITLE}': {e}")
        return

    counter = 0

    def capture():
        with mss.mss() as sct:
            monitor = {
                "top": rect.top,
                "left": rect.left,
                "width": rect.width(),
                "height": rect.height()
            }
            img = np.array(sct.grab(monitor))
            if img.shape[2] == 4:
                img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            filename = os.path.join(
                SAVE_DIR, f"screenshot_{int(time.time())}.png")
            cv.imwrite(filename, img)
            print(f"Saved {filename}")

    keyboard.add_hotkey(hotkey, capture)
    print(
        f"Press '{hotkey}' key to capture the window '{APP_TITLE}'. Press Ctrl+C to exit.")
    keyboard.wait()


if __name__ == "__main__":
    main()
