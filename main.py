#!/usr/bin/python3
"""
 Test cities access from a state
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

"""
 Objects creations
"""
state_1 = State(name="California")
state_1.save()
state_2 = State(name="Arizona")
state_2.save()

city_1_1 = City(state_id=state_1.id, name="Napa")
city_1_1.save()
city_1_2 = City(state_id=state_1.id, name="Sonoma")
city_1_2.save()
city_2_1 = City(state_id=state_2.id, name="Page")
city_2_1.save()

amenity_1 = Amenity(name="Wifi")
amenity_1.save()


"""
 Verification
"""
print("")
all_states = storage.all(State)
for state_id, state in all_states.items():
    for city in state.cities:
        print("Find the city {} in the state {}".format(city, state))
