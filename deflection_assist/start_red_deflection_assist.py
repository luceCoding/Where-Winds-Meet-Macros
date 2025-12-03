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
from tools.capture_image import get_monitor


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
    lower_hsv_color_filter = config["lower_hsv_color_filter"]
    upper_hsv_color_filter = config["upper_hsv_color_filter"]
    threshold_low, threshold_high = config["white_pixel_threshold_range"]
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

    monitor = get_monitor(game, partial_percent=0.1)

    # Create persistent mss instance
    with mss.mss() as sct:

        n_red_frames = 0

        while not stop_flag["stop"]:
            img = cv.cvtColor(np.array(sct.grab(monitor)), cv.COLOR_BGRA2BGR)

            gray_color_only = preprocess_color_only(img, 
                                                    lower_hsv_color_filter, 
                                                    upper_hsv_color_filter,
                                                    )

            _, binary = cv.threshold(gray_color_only, 20, 255, cv.THRESH_BINARY)
            percent_white = pixel_percent_white(binary)

            if percent_white >= threshold_low and percent_white <= threshold_high:
                #print(f"Percent of white pixels: {percent_white:.3f}%")
                n_red_frames += 1
                if n_red_frames >= frame_delay:
                    game.send_keystrokes(key_deflection)
                    #print(f"Deflection!")
            elif percent_white < threshold_low:
                n_red_frames = 0 # No more red frames, reset


if __name__ == "__main__":
    main()
