#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    """Get the list of cities associated with the State object"""
    city_list = obj_state.cities

    city_dicts = []
    """Convert each city to a dictionary"""
    for city in city_list:
        city_dicts.append(city.to_dict())

    return jsonify(city_dicts), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """Retrieves a City object by his id"""
    obj_city_id = storage.get(City, city_id)
    if obj_city_id is None:
        abort(404)
    return jsonify(obj_city_id.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    """Delete a City object by his id"""
    empty = {}
    obj_city_id = storage.get(City, city_id)
    if obj_city_id is None:
        abort(404)
    storage.delete(obj_city_id)
    storage.save()
    return (jsonify(empty), 200)


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_create(state_id):
    """Returns the new City with the status code 201"""
    data = request.get_json()

    """Get the State object by its ID"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    if data is None:
        return "Not a JSON\n", 400
    elif "name" not in data:
        return "Missing name\n", 400
    else:
        """Create a new City object"""
        obj = City()
        obj.name = data["name"]
        obj.state_id = state_id
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update(city_id):
    """Update a City object by his id"""
    obj_update = storage.get(City, city_id)
    if obj_update is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        else:
            for key, value in data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(obj_update, key, value)
            storage.save()

        return jsonify(obj_update.to_dict()), 200
