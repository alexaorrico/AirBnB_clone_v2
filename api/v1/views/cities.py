#!/usr/bin/python3
""" creates a new view for State object """
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ get list of cities """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = storage.all(City).values()
    cities_all = []
    for city in cities:
        cities_all.append(city.to_dict())
    return jsonify(cities_all)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ get list by id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ deletes a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def post_city():
    """ post method for adding city """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    res = request.get_json()
    city = City(**res)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_state(city_id):
    """ updates city based on id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")
    fields = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in fields:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
