#!/usr/bin/python3
""" States RESTful API """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Retrieves all cities of a State object, or returns a 404 if
     the state_id is not linked to any object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    cities = state.cities
    list = []
    for city in cities:
        list.append(city.to_dict())
    return jsonify(list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """ Retrieves a City object, or returns a 404 if
    the city_id is not linked to any object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object, or returns a 404 if the city_id is not
    linked to any object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City object, or returns a 400 if the HTTP body request is not
    valid JSON, or if the dict doesn't contain the key name """
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    name = data.get("name")
    if name is None:
        abort(400, "Missing name")
    if storage.get("State", state_id) is None:
        abort(404)

    new_city = City()
    new_city.name = name
    new_city.state_id = state_id
    new_city.save()
    return (jsonify(new_city.to_dict())), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object, or returns a 400 if the HTTP body is not valid
    JSON, or a 404 if state_id is not linked to an object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return (jsonify(city.to_dict()))
