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
