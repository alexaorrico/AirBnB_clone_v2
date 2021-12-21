#!/usr/bin/python3
'''create route for cities'''
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        res = []
        for obj in state.cities:
            res.append(obj.to_dict())
        return jsonify(res)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    city_dict = request.get_json()
    if not state:
        abort(404)
    elif not city_dict:
        abort(400, "Missing name")
    else:
        city = City(**city_dict)
        city.state_id = state.id
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_dict = request.get_json()
    if not city_dict:
        abort(400, "Not a JSON")
    for key in city_dict:
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, city_dict[key])
    city.save()
    return jsonify(city.to_dict()), 200
