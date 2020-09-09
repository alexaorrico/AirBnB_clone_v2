#!/usr/bin/python3
"""cutty sark"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request, Blueprint


@app_views.route('/states/<state_id>/cities')
def get_cities(state_id):
    """return list of all cities in state"""
    lizt = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        lizt.append(city.to_dict())
    return jsonify(lizt)


@app_views.route('/cities/<city_id>')
def get_a_city(city_id):
    """retrieve of specific City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    ret = city.to_dict()
    return jsonify(ret)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_a_city(city_id):
    """delete a specific city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
