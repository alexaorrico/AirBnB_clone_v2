#!/usr/bin/python3
"""the views documentation"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place  import Place
from models.review  import Review
from models.user import User
@app_views.route('/status', strict_slashes=False)
def status():
    """returns the status of an API"""
    j = {
            "status": "OK"
        }
    return j

@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns number of each class"""
    stats = {
              "amenities": 0, 
              "cities": 0, 
              "places": 0, 
              "reviews": 0, 
              "states": 0, 
              "users": 0
            }
    amenities =  storage.count(Amenity)
    cities =  storage.count(City)
    places =  storage.count(Place)
    reviews =  storage.count(Review)
    states =  storage.count(State)
    users =  storage.count(User)
    stats.update({
              "amenities": amenities,
              "cities": cities,
              "places": places,
              "reviews": reviews,
              "states": states,
              "users": users
              })
    return stats
