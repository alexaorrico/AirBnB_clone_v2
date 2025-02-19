from models import storage
from models.state import State

new_state = State(name="California")
storage.new(new_state)
storage.save()
print("State added with id:", new_state.id)
