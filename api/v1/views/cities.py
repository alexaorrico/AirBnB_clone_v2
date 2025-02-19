#!/usr/bin/python3

"""
This module is for State objects that handles all
default RESTFul API actions
"""
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def city(state_id):
    """
    states get the list of all state objects
    """
    obj = storage.all(City)
    lis = []

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for key, value in obj.items():
        if value.state_id == state_id:
            cty = obj[key]
            lis.append(cty.to_dict())
    return jsonify(lis)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_obj(city_id):
    """
    Get's object of State using id e.g (8f165686-c98d-46d9-87d9-d6059ade2d99)
    """
    obj = storage.all(City)
    try:
        for key, value in obj.items():
            if value.id == city_id:
                return jsonify(value.to_dict())
        abort(404)
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """
    DELETE State with id (city_id)
    """
    obj = storage.all(City)
    try:
        for key, value in obj.items():
            if value.id == city_id:
                storage.delete(value)
                storage.save()
                empty = {}
                return jsonify(empty), 200
        abort(404)
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    POST to State with body or content of request
    """

    data = request.get_json()
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if data is None:
        abort(400, description="Not a JSON")

    if not data.get('name'):
        abort(400, description="Missing name")

    else:
        new_obj = City()
        new_obj.state_id = state_id
        new_obj.name = data.get('name')
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(state_id):
    """
    PUT to update State with body or content of request
    """
    data = request.get_json()

    # Check if JSON is provided
    if data is None:
        abort(400, description="Not a JSON")

    # Retrieve the state object by ID
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    # Update state object with provided data
    for name, val in data.items():
        if name not in ('id', 'created_at', 'updated_at'):
            setattr(city, name, val)

    # Save changes to the storage
    storage.save()

    return jsonify(city.to_dict()), 200
