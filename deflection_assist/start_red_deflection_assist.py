import os
import psutil
import cv2 as cv
import numpy as np
import mss
from pywinauto.application import Application
import keyboard
import yaml
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.plot_image_thresholds import pixel_percent_white, preprocess_color_only


def main():

    p = psutil.Process(os.getpid())
    p.cpu_affinity([0])  # force script to core 0 only
    p.nice(psutil.HIGH_PRIORITY_CLASS)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    app_title = config["app_title"]
    key_stop_script = config["key_stop_script"]
    key_deflection = config["key_deflection"]
    white_pixel_threshold_range = config["white_pixel_threshold_range"]
    frame_delay = config["frame_delay"]

    try:
        app = Application().connect(title=app_title, found_index=0)
        game = app[app_title]
        rect = game.rectangle()
        print("Game application found. Starting script.")
    except Exception as e:
        print(f"Error: Game application not found: {e}")
        sys.exit(1)

    stop_flag = {"stop": False}
    keyboard.add_hotkey(
        key_stop_script, lambda: stop_flag.update({"stop": True}))

    # Create persistent mss instance
    with mss.mss() as sct:
        monitor = {
            "top": rect.top,
            "left": rect.left,
            "width": rect.width(),
            "height": rect.height()
        }

        n_red_frames = 0

        while not stop_flag["stop"]:
            img = np.array(sct.grab(monitor))
            img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

            gray_color_only = preprocess_color_only(img, 
                                                    [0, 50, 255], 
                                                    [10, 200, 255],
                                                    )

            percent_white = pixel_percent_white(gray_color_only)

            if percent_white >= white_pixel_threshold_range[0] and percent_white <= white_pixel_threshold_range[1]:
                print(f"Percent of white pixels: {percent_white:.3f}%")
                n_red_frames += 1
                if n_red_frames >= frame_delay:
                    game.send_keystrokes(key_deflection)
                    print(f"Deflection!")
            elif percent_white < white_pixel_threshold_range[0]:
                n_red_frames = 0


if __name__ == "__main__":
    main()
