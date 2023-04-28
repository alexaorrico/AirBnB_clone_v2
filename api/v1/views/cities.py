#!/usr/bin/python3
"""Creates a view for City objects"""

import json
from models import storage
from models.city import City
from models.state import State
from api.v1.views import city_views
from flask import abort, make_response, request, jsonify


@city_views.errorhandler(400)
def handle400(exception):
    """handles 400 errors"""
    return make_response(jsonify(exception.description)), 400


@city_views.route('/states/<state_id>/cities', methods=['GET'],
                  strict_slashes=False)
def get_all_cities(state_id):
    """gets all the cities associated with the state_id"""
    print(state_id)
    cities = storage.all(City)
    cities_obj = []
    for city in cities.values():
        if city.state_id == state_id:
            cities_obj.append(city.to_dict())
    if len(cities_obj) == 0:
        abort(404)
    return jsonify(cities_obj)


@city_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """gets a single city"""
    cities = storage.all(City)
    city = None
    for c in cities.values():
        if c.id == city_id:
            city = c.to_dict()
    if city is None:
        abort(404)
    return jsonify(city)


@city_views.route('/cities/<city_id>', methods=['DELETE'],
                  strict_slashes=False)
def delete_city(city_id):
    """deletes a city from db"""
    cities = storage.all(City)
    city = None
    for c in cities.values():
        if c.id == city_id:
            city = c
            break
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({})


@city_views.route('states/<state_id>/cities', methods=['POST'],
                  strict_slashes=False)
def post_city(state_id):
    """adds a new city to the db"""
    states = storage.all(State)
    state = None
    for s in states.values():
        if s.id == state_id:
            state = s
            break
    if state is None:
        abort(404)

    try:
        data = json.loads(request.data)
    except (ValueError, KeyError, TypeError):
        abort(400, description="Not a JSON")

    if 'name' not in request.json:
        abort(400, description="Missing name")
    city = request.get_json()
    new_city = City(state_id=state_id, name=city['name'])
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@city_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city"""
    cities = storage.all(City)
    city = None
    for c in cities.values():
        if c.id == city_id:
            city = c
            break
    if city is None:
        abort(404)

    try:
        data = json.loads(request.data)
    except (ValueError, TypeError, KeyError):
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key in data.keys():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, data[key])
    city.save()
    return jsonify(city.to_dict())
