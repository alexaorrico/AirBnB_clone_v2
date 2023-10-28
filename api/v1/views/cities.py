#!/usr/bin/python3
'''Contains the cities view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects of a State"""
    all_cities = storage.get(State, state_id)
    if not all_cities:
        abort(404)
    return jsonify([city.to_dict() for city in all_cities.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def single_city(city_id):
    """Retrieves a City object"""
    one_city = storage.get(City, city_id)
    if not one_city:
        abort(404)
    return jsonify(one_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Returns an empty dictionary with the status code 200"""
    city_deleted = storage.get(City, city_id)
    if not city_deleted:
        abort(404)
    city_deleted.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Returns the new City with the status code 201"""
    city_state = storage.get(State, state_id)
    if not city_state:
        abort(404)

    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if 'name' not in new_city:
        abort(400, "Missing name")

    obj = City(**new_city)
    setattr(obj, 'state_id', state_id)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Returns the City object with the status code 200"""
    new_city = storage.get(City, city_id)
    if not new_city:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'created_at', 'update_at', 'state_id']:
            setattr(new_city, k, v)

    storage.save()
    return make_response(jsonify(new_city.to_dict()), 200)
