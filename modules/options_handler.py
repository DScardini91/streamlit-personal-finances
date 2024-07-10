import json


def load_options():
    with open("modules/options.json", "r") as f:
        options = json.load(f)
    return options


def save_options(options):
    with open("modules/options.json", "w") as f:
        json.dump(options, f, indent=4)
