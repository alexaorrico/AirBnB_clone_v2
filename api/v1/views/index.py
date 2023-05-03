#!/usr/bin/python3
"""This returns the api status"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """This returns our status if successfully connected"""
    return jsonify({'status': "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """This returns our stats if successfully connected"""
    end = {}
    end['amenities'] = storage.count(Amenity)
    end['cities'] = storage.count(City)
    end['places'] = storage.count(Place)
    end['reviews'] = storage.count(Review)
    end['states'] = storage.count(State)
    end['users'] = storage.count(User)
    return jsonify(end)
