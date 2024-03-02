#!/usr/bin/python3
""" New City view """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
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
        return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def one_city(city_id):
    """ Returns one city """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city object """
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a new city obj using a state_id """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    if storage.get(State, state_id):
        data['state_id'] = state_id
        obj = City(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Updates a city package """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    obj = storage.get(City, city_id)
    if obj:
        for key, value in data.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(obj, key, value)
        obj.save()
        return jsonify(obj.to_dict()), 200
    abort(404)
