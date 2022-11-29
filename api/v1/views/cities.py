#!/usr/bin/python3
"""module states - handles states objects for RestfulAPI"""
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """retrieves list of city objects by state"""
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """retrieves specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes city object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city():
    """creates city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, descritpion="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.state_id = state.id
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """updates city object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id' 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
