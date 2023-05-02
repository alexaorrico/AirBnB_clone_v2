#!/usr/bin/python3
import json
from models.state import State
from models import storage

with open("file.json", "r") as f:
    data = json.load(f)

for state_data in data["states"]:
    state = State(**state_data)
    storage.new(state)

storage.save()
