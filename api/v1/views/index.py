#!/usr/bin/python3
"""Return status """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route("/status", methods=['GET'])
def return_status():
    """Return status of GET request"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def return_count():
    ''' Retrieve the number of each object by type '''
    return jsonify({
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
        })
