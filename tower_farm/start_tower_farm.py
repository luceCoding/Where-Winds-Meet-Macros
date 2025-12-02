from pywinauto.application import Application
import keyboard
import yaml
import time
import os

# ------------------------------
# Load config
# ------------------------------

# Get the directory where THIS script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the full path to config.yaml in that directory
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.yaml")

# Load config
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Unpack config
(
    app_title,
    key_meteor_flight,
    key_fly,
    key_land,
    key_call_horse,
    key_fan_heal,
    key_dragons_breath,
    key_stop_script
) = (
    config['app_title'],
    config['key_meteor_flight'],
    config['key_fly'],
    config['key_land'],
    config['key_call_horse'],
    config['key_fan_heal'],
    config['key_dragons_breath'],
    config['key_stop_script']
)

# ------------------------------
# Connect to app
# ------------------------------
try:
    app = Application().connect(title=app_title, found_index=0)
    game = app[app_title]
    print("Game application found. Starting script.")
except Exception:
    print("Error: Game application not found!")
    exit()


# ------------------------------
# Stop flag + hotkey
# ------------------------------
stop_script = False

def stop():
    global stop_script
    stop_script = True
    print("Stop key pressed — stopping program...")

keyboard.add_hotkey(key_stop_script, stop)


# ------------------------------
# Helper: run steps safely
# ------------------------------
def run_step(action, sleep_time=0):
    """
    Executes a keystroke action with optional sleep,
    automatically stops if stop flag is triggered.
    """
    if stop_script:
        return False

    if isinstance(action, str):
        game.send_keystrokes(action)
    else:
        # list of actions
        for a in action:
            game.send_keystrokes(a)

    if sleep_time:
        for _ in range(int(sleep_time * 10)):  # check stop every 0.1s
            if stop_script:
                return False
            time.sleep(0.1)
    return True


# Pre-formatted meteor flight hold commands
meteor_down = f"{{{key_meteor_flight} DOWN}}"
meteor_up   = f"{{{key_meteor_flight} UP}}"

# ------------------------------
# Main Loop
# ------------------------------
n_rotations = 0

while not stop_script:

    steps = [
        ([meteor_down, meteor_up], 1.75),   # Start Meteor Flight
        ([key_fly, key_fly],        3.5),   # Continue Flight
        ([key_land] * 4,            2.5),   # Land spam
        (key_call_horse,            1.75),  # Call horse
        (key_dragons_breath,        3),     # Breath
        (key_fan_heal,              8),     # Heal
    ]

    for action, delay in steps:
        if not run_step(action, delay):
            break

    n_rotations += 1
    print(f"Run {n_rotations} completed.")