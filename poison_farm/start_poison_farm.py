from pywinauto.application import Application
import yaml
import time

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

app_title = config['app_title']
key_meteor_flight = config['key_meteor_flight']
key_fly = config['key_fly']
key_land = config['key_land']
key_call_horse = config['key_call_horse']
key_fan_heal = config['key_fan_heal']
key_dragons_breath = config['key_dragons_breath']

app = Application().connect(title=app_title, found_index=0)

if app is not None:

    print("Game application found. Starting script.")

    game = app[app_title]
    meteor_flight_held_down = "{" + f"{key_meteor_flight}" + " DOWN}"
    meteor_flight_held_up = "{" + f"{key_meteor_flight}" + " UP}"
    n_rotations = 0

    while True:

        game.send_keystrokes(meteor_flight_held_down) # Start Meteor Flight
        game.send_keystrokes(meteor_flight_held_up)
        time.sleep(1.75)
        game.send_keystrokes(key_fly)
        game.send_keystrokes(key_fly)
        time.sleep(3)
        game.send_keystrokes(key_land) # Land on ground
        game.send_keystrokes(key_land) # Land on ground
        time.sleep(2.75)
        game.send_keystrokes(key_call_horse) # Call horse
        time.sleep(1.75)
        game.send_keystrokes(key_fan_heal) # Fan Heal
        time.sleep(1.5)
        game.send_keystrokes(key_dragons_breath) # Dragon's Breath
        time.sleep(11)
        n_rotations += 1
        print(f"Run {n_rotations} completed.")

else:
    print("Error: Game application not found!")