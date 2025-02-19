#!/usr/bin/python3
from models.state import State
from models import storage

# Create a new State object
new_state = State(name="California")

# Add the new state to storage
storage.new(new_state)
storage.save()  # Save changes

print("New state added: {}".format(new_state))

