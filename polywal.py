#!/usr/bin/python3

# =================================================
#               .__                         .__   
# ______   ____ |  | ___.__.__  _  _______  |  |  
# \____ \ /  _ \|  |<   |  |\ \/ \/ /\__  \ |  |  
# |  |_> >  <_> )  |_\___  | \     /  / __ \|  |__
# |   __/ \____/|____/ ____|  \/\_/  (____  /____/
# |__|               \/                   \/      
#
#    fork by localdumbkat ; original by luishgh
#     https://github.com/localdumbkat/polywal
#
# =================================================
# 
# polywal is a helpful Python script that allows you
# to easily change the colors of your polybar config
# file based on the colors generated by pywal.
#
# =================================================

import os
import sys
import subprocess
import configparser

# paths
WAL_COLOR_PATH=os.path.expanduser("~/.cache/wal/colors")
GLOBAL_POLYBAR_CONFIG=os.path.expanduser("/etc/polybar/config.ini")
LOCAL_POLYBAR_CONFIG=os.path.expanduser("~/.config/polybar/config.ini")

# variables
config = {
    "use_global": False,
    "profile": None,
    "backup": False,
}

# builtin profiles (WHERE VALS ARE 1-16)
profile1 = {
    "name": "profile1",
    "colors": {
        "background": "1",
        "background-alt": "3",
        "foreground": "2",
        "primary": "5",
        "secondary": "4",
        "alert": "8",
    }
}
profile2 = {
    "name": "profile2",
    "colors": {
        "background": "2",
        "background-alt": "4",
        "foreground": "5",
        "primary": "8",
        "secondary": "7",
        "alert": "8",
    }
}
profile3 = {
    "name": "profile3",
    "colors": {
        "background": "#ff0000",
        "background-alt": "#ff0000",
        "foreground": "#00ff00",
        "primary": "#00ff00",
        "secondary": "#ff0000",
        "alert": "#0000ff",
    }
}

def read_wal_colors() -> list[str]:
    try:
        with open(WAL_COLOR_PATH, 'r') as f:
            return [line for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: Could not find wal colors file.")
        sys.exit(1)
    
def create_backup(config: dict):
    if config["use_global"]:
        config_path = GLOBAL_POLYBAR_CONFIG
    else:
        config_path = LOCAL_POLYBAR_CONFIG

    with open(config_path, 'r') as f:
        with open(config_path + ".bak", 'w') as f2:
            f2.write(f.read())

# main function
def main():
    global config
    
    # if global flag is set, use the global polybar config
    if "-g" in sys.argv or "--global" in sys.argv:
        config["use_global"] = True

    # if profile flag is set, set the profile, otherwise default to profile 1
    if "-p1" in sys.argv or "--profile1" in sys.argv:
        config["profile"] = profile1
    elif "-p2" in sys.argv or "--profile2" in sys.argv:
        config["profile"] = profile2
    elif "-p3" in sys.argv or "--profile3" in sys.argv:
        config["profile"] = profile3
    else:
        config["profile"] = profile1 # default to profile 1

    # if backup flag is set, create a backup of the config file
    if "-b" in sys.argv or "--backup" in sys.argv:
        config["backup"] = True
        create_backup(config)

    # read the colors from the wal cache
    colors = read_wal_colors()

    # config
    polybar_config = configparser.ConfigParser()

    if config["use_global"]:
        try:
            polybar_config.read(GLOBAL_POLYBAR_CONFIG)
        except:
            print("Error: Could not read global polybar config file.")
            sys.exit(1)
    else:
        try:
            if not os.path.exists(LOCAL_POLYBAR_CONFIG): # file is not found
                print("polywal did not find a local polybar config file.")
                print("polywal will create a new config file.")
                tf = open(LOCAL_POLYBAR_CONFIG, 'w')
                tf.write("[colors]\n")
                print("created new config file, please run polywal again.")
                sys.exit(1)
            else: # file is found
                polybar_config.read(LOCAL_POLYBAR_CONFIG)
        except:
            print("Error: Could not read local polybar config file.")
            sys.exit(1)
    
    # update the program config with the new colors
    if polybar_config.has_section("colors"):
        for key, value in config["profile"]["colors"].items():
            try:
                polybar_config["colors"][key] = colors[int(value) - 1]
            except IndexError: # fix index out of range error
                polybar_config["colors"][key] = 1
    else:
        polybar_config["colors"] = config["profile"]["colors"]

    # write the new config to the polybar config file
    if config["use_global"]:
        try:
            with open(GLOBAL_POLYBAR_CONFIG, 'w') as f:
                polybar_config.write(f)
        except PermissionError:
            print("polywal failed to write to global polybar config file.")
            print("Try running polywal with sudo.")
            sys.exit(1)
        else:
            print("polywal wrote to global polybar config")
    else:
        with open(LOCAL_POLYBAR_CONFIG, 'w') as f:
            polybar_config.write(f)
            print("polywal wrote to local polybar config file.")
        

if __name__ == '__main__':
    main()
