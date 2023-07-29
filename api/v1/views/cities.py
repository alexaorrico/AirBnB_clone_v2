#!/usr/bin/python3
"""
view for the cities
"""
from models import storage
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_state(state_id):
    """Retrieve all city objects related to state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Create new city object"""
    post_req = request.get_json()
    if not post_req:
        abort(400, "Not a JSON")
    if "name" not in post_req:
        abort(400, "Missing name")

    __state = storage.get(State, state_id)
    if not __state:
        abort(404)

    new_city = City(**post_req)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(new_city.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update a city object with the provided city id"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a  JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    ignore_keys = ['id', 'created_id', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
