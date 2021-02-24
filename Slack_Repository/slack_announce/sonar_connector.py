import json

with open("slack_announce/dev.json", "r") as json_file:
    measure = json.load(json_file)


def get_measure(project_key):
    return measure
