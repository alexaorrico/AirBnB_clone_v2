#!/usr/bin/python3
"""   module that creates a new view for City objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves all the City objects linked to a state_id """
    state = storage.get(State, state_id)
    list_cities = []
    if state:
        for city in state.cities:
            list_cities.append(city.to_dict())
            return jsonify(list_cities)
    else:
            abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    empty_dict = {}
    city.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, "Not a JSON")
    elif "name" not in my_dict:
        abort(400, "Missing name")
    my_dict["state_id"] = state_id
    new_city = City(**my_dict)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    if city_id:
        my_dict = request.get_json()
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if my_dict is None:
            abort(400, "Not a JSON")
        for key, value in my_dict.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
