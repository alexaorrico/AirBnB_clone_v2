#!/usr/bin/python3
"""commandant"""
from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def status():
    """jsonify my life"""
    return jsonify({'status': 'OK'})

"""@app_views.route('/api/v1/stats')
def stats():
    commenr
    returnjsonify({'amenities': storage.count(Amenity),
                    'cities': storage.count(City),
                    'places': storage.count(Place),
                    'reviews': storage.count(Review),
                    'states': storage.count(State)
                    'users': storage.count(User)})
"""
