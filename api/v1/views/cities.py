#!/usr/bin/python3
"""
script that starts a Flask web application:
"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def city_all(state_id=None):
    """
    Retrieves a city object:
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return (jsonify(all_cities), 200)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_a(city_id=None):
    """
    Retrieves a city object:
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id=None):
    """
    Deletes a State object
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """
    Creates a State
    """
    my_city = request.get_json()
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        my_city['state_id'] = state.id
        city = City(**my_city)
        city.save()
        resp = jsonify(city.to_dict())
        return (resp), 201
    abort(404)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """
    Updates a State object
    """
    st = request.get_json()
    if st is None:
        abort(400, "Not a JSON")
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    else:
        city.name = st['name']
        city.save()
        return (jsonify(city.to_dict()), 200)
