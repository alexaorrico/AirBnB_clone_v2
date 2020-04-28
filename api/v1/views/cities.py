#!/usr/bin/python3
"""
Handles all default RestFul API actions for cities
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id=None):
    ''' Retrieves a list of all city objects of a given state '''
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    cities = storage.all('City')
    city_list = []
    for val in cities.values():
        if val.state_id == state_id:
            city_list.append(val.to_dict())

    return jsonify(city_list)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    ''' returns an individual city object '''
    obj = storage.get('City', city_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    ''' deletes an individual city '''
    obj = storage.get('City', city_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"],
                 strict_slashes=False)
def create_city(state_id=None):
    ''' create a city if doesn't already exist '''
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in args:
        return jsonify({"error": "Missing name"}), 400
    args['state_id'] = state_id
    obj = City(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    ''' updates an individual city '''
    obj = storage.get('City', city_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)

    args = request.get_json()

    if args is None:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in args.items():
        if k not in ["id", "state_id", "updated_at", "created_at"]:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
