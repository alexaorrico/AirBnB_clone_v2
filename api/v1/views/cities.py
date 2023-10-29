#!/usr/bin/python3
""" STATE VIEW """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models import storage
from models.state import State


@app_views.route(
        '/states/<state_id>/cities', methods=["GET"], strict_slashes=False
        )
def all_state_cities(state_id):
    """ Return all state cities objects in the DB """
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route(
        '/cities/<city_id>', methods=["GET"], strict_slashes=False
        )
def single_city(city_id):
    """ Returns city that matches with provided ID """
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/cities/<city_id>', methods=["DELETE"], strict_slashes=False
        )
def delete_city(city_id):
    """ Deletes city that matches with provided ID """
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route(
        '/states/<state_id>/cities', methods=["POST"], strict_slashes=False
        )
def add_city(state_id):
    """ Adds city object to DB """
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if "name" not in data:
        abort(400, 'Missing name')

    data["state_id"] = state.id
    new_city = City(**data)
    storage.save()
    res = jsonify(new_city.to_dict())
    res.status_code = 201
    return res


@app_views.route(
        '/cities/<city_id>', methods=["PUT"], strict_slashes=False
        )
def update_city(city_id):
    """Updates city object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    for key, val in data.items():
        if key not in ["state_id", "id", "updated_at", "created_at"]:
            setattr(city, key, val)
    storage.save()
    return jsonify(city.to_dict())
