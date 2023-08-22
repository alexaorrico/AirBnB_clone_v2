#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
from models import storage
from models.state import State                                                  
from models.amenity import Amenity                                              
from models.city import City                                                    
from models.user import User                                                    
from models.place import Place
from models.review import Review


@app_views.route('/status')
def status():
    """return status ok"""
    return {
        "status": "OK"
        }

@app_views.route('/stats')
def count():
    """return counts"""
    return {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    