#!/usr/bin/python3
""" New City view """

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Returns all cities linked to a particular city """
    city_objs = storage.all(City)
    cities = []
    for obj in city_objs.values():
        if obj.state_id == state_id:
            cities.append(obj.to_dict())
    if len(cities) == 0:
        abort(404)
    else:
        return jsonify(cities), 200


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def one_city(city_id):
    """ Returns one city """
    
