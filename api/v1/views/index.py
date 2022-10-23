#!/usr/bin/pyton3
"""
create a route status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methodes=['GET'])
def json_string(self):
    """ return the JSON representation of the status of the flask"""
    new = {'status': 'OK'}
    return jsonify(new)


@app_views.route('/stats', methods=['GET'])
def obj_by_count():
    """retrieves the number of each objects by type """
    new = {}
    cls_dict = {'amenities': Amenity, 'cities': City, 'places': Place,
                'reviews': Review, 'states': State, 'users': User}

    for key, val in cls_dict.items():
        new[key] = storage.count(val)

    return jsonify(new)
