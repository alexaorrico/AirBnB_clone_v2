#!/usr/bin/python3
from models.engine.db_storage import DBStorage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import models

# Initialize storage
storage = DBStorage()
storage.reload()

# Create initial data
state = State(name="California")
city = City(name="San Francisco", state_id=state.id)
user = User(email="user@example.com", password="password")
place = Place(name="Beautiful Apartment", city_id=city.id, user_id=user.id)
amenity = Amenity(name="Wi-Fi")
review = Review(text="Great place!", place_id=place.id, user_id=user.id)

# Add data to storage
storage.new(state)
storage.new(city)
storage.new(user)
storage.new(place)
storage.new(amenity)
storage.new(review)

# Save changes
storage.save()
