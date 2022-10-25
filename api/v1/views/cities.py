#!/usr/bin/python3
"""Create a new view for Cities objects that handles all default RESTFul API
actions"""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_all_cities(state_id):
    """Retrieves all the cities of a given state_id"""
    for state in storage.all(State).values():
        if state.id == state_id:
            list_city = []
            for city in state.cities:
                list_city.append(city.to_dict())
            return jsonify(list_city)
    return abort(404)


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities_with_id(city_id):
    """Methods that retrieves all methods for cities with id"""

    if request.method == 'GET':
        """Retrieves a city of a given city_id"""
        for city in storage.all(City).values():
            if city.id == city_id:
                return jsonify(city.to_dict())
        return abort(404)

    if request.method == 'DELETE':
        """Deletes a city of a given city_id """
        for city in storage.all(City).values():
            if city.id == city_id:
                city.delete()
                storage.save()
                return jsonify({})
        return abort(404)

    if request.method == 'PUT':
        """Updates a city of a given city_id"""
        city = storage.get(City, city_id)
        if city is None:
            return abort(404)

        r = request.get_json()
        if r is None:
            return abort(400, 'Not a JSON')
        toIgnore = ["id", "created_at", "updated_it"]
        for key, value in r.items():
            if value not in toIgnore:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_one_city(state_id):
    """Creates one city tied with the given state_id based on the JSON body"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    r = request.get_json()
    if r is None:
        return abort(400, 'Not a JSON')
    if r.get('name') is None:
        return abort(400, 'Missing name')
    r['state_id'] = state.id
    new = City(**r)
    new.save()
    return jsonify(new.to_dict()), 201
