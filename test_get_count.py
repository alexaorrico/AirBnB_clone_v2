from models import storage
from models.state import State

# Count all objects
all_objects_count = storage.count()

# Count State objects
state_objects_count = storage.count(State)

# Retrieve the first state object directly without fetching all State objects first
first_state = storage.get(State, first=True)

print("All objects: {}".format(all_objects_count))
print("State objects: {}".format(state_objects_count))
print("First state: {}".format(first_state))
