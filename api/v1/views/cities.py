#!/usr/bin/python3
""" Module to handle cities RESFful API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_city(state_id):
    states = storage.all(State).values()
    cities = storage.all(City).values()

    state = [state for state in states if state.id == state_id]
    if len(state) == 0:
        abort(404)

    if request.method == 'GET':
        new_list = []
        for city in cities:
            if city.state_id == state_id:
                new_list.append(city.to_dict())
        return jsonify(new_list)

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_dict = request.get_json()
        new_dict['state_id'] = state_id
        obj = City(**new_dict)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def one_city(city_id):
    cities = storage.all(City).values()
    city = [city for city in cities if city.id == city_id]
    if len(city) == 0:
        abort(404)

    if request.method == 'GET':
        return city[0].to_dict()

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.get_json().items():
            if k != 'id' and k != 'created_at'\
               and k != 'updated_at' and k != 'state_id':
                setattr(city[0], k, v)
        storage.save()
        return jsonify(city[0].to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(city[0])
        storage.save()
        return {}, 200
