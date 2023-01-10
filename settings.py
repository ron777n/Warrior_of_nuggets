"""
handles the settings
"""
import json

with open("settings.json") as f:
    settings = json.load(f)

Screen = \
    {
        "Size": [settings["Screen"]["Size"]]
    }

