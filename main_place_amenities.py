#!/usr/bin/python3
""" Test link Many-To-Many Place <> Amenity
"""
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity

# creation of a State
state = State(name="California")
state2 = State(name="Alabama")
state2.save()
state.save()

# creation of a City
city = City(state_id=state.id, name="San Francisco")
city1 = City(state_id=state2.id, name="Tupelo")
city1.save()
city.save()

# creation of a User
user = User(email="john@snow.com", password="johnpwd")
user1 = User(email="ermiyas@abiye.com", password="ermipwd")
user1.save()
user.save()

# creation of 2 Places
place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
place_1.save()
place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
place_2.save()
place_3 = Place(user_id=user1.id, city_id=city1.id, name="House 3")
place_3.save()

# creation of 3 various Amenity
amenity_1 = Amenity(name="Wifi")
amenity_1.save()
amenity_2 = Amenity(name="Cable")
amenity_2.save()
amenity_3 = Amenity(name="Oven")
amenity_3.save()

# link place_1 with 2 amenities
place_1.amenities.append(amenity_1)
place_1.amenities.append(amenity_2)

# link place_2 with 3 amenities
place_2.amenities.append(amenity_1)
place_2.amenities.append(amenity_2)
place_2.amenities.append(amenity_3)

place_3.amenities.append(amenity_1)
place_3.amenities.append(amenity_2)
place_3.amenities.append(amenity_3)

storage.save()

print("OK")
