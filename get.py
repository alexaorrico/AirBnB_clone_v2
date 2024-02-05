#!/usr/bin/python3
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


amenity = storage.get(Amenity, "89fa5b1d-221d-4fdb-98cd-45673dd8b52a")

amenity.name = "new_name"
print(amenity.to_dict())


