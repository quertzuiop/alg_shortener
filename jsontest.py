import json
import os

with open("cube_states.json", "r") as f:
    data = json.load(f)
    for i in range(len(data.keys())-2):
        print(len(data[str(i)]))
