#!/usr/bin/python3
""" script for State view """

from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort
from flask import request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities_of_state(state_id):
    """Route list of all city object of state"""
    stat_obj = storage.get(State, state_id)
    if not stat_obj:
        abort(404)

    list_city = []
    for city in stat_obj.cities:
        list_city.append(city.to_dict())

    return make_response(jsonify(list_city), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Route that returns city by id"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    return make_response(jsonify(city_obj.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    """ delete http request"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """post http request """
    stat_obj = storage.get(State, state_id)
    if not stat_obj:
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400, description="Not a JSON")
    if 'name' not in request_dict:
        abort(400, description="Missing name")
    request_dict['state_id'] = state_id
    obj = City()

    for k, v in request_dict.items():
        setattr(obj, k, v)

    # add obj to current DB session and save it.
    storage.new(obj)
    storage.save()
    new_state = obj.to_dict()
    return make_response(jsonify(new_state), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update(city_id):
    """put http request"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    new_dict = request.get_json()
    if not new_dict:
        abort(400, description="Not a JSON")

    new_dict = request.get_json()
    ignore_keys = {'id', 'created_at', 'updated_at'}
    for k, v in new_dict.items():
        if k not in ignore_keys:
            setattr(city_obj, k, v)

    storage.save()
    return make_response(jsonify(city_obj.to_dict()), 200)
