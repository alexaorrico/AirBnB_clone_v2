#!/usr/bin/python3

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

mapped_classes = {"User" : User, "State" : State, "Review" : Review, "Place" : Place, "City" : City, "Amenity" : Amenity }