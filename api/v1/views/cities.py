#!/usr/bin/python3
"""
text
"""
from models import storage
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def states(state_id=None):
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    else:
        cities = []
        for city in states.cities:
            cities.append(city.to_dict())
        return jsonify(cities)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def cities(city_id=None):
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    else:
        return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_cities(city_id=None):
    """
    remove city that has specific id
    """
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return None
