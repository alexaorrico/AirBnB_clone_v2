#!/usr/bin/python3
from models import storage
from models.state import State

# Create new State objects
state1 = State(name="Colorado")
state2 = State(name="Arizona")

# Add and save the State objects
storage.new(state1)
storage.new(state2)
storage.save()

print("States added to the storage.")
