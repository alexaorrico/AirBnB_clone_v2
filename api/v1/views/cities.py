#!/usr/bin/python3

""" Module handling requests for City objects """

from models import storage
from api.v1.views import app_views
from models.state import State, City
from flask import request, jsonify, abort

ignored_keys = ['id', 'created_at', 'updated_at', 'state_id']


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST', 'POST'])
def all_cities(state_id):
    """ Handles GET and POST request for all city """
    state_obj = storage.all(State)
    for key, val in state_obj.items():
        if val.id == state_id:
            if request.method == 'GET':
                city_obj = storage.all(City)
                city_list = []
                for key, val in city_obj.items():
                    if val.state_id == state_id:
                        city_list.append(val.to_dict())
                return jsonify(city_list)

            if request.method == 'POST':
                cities = City()
                data = request.get_json(silent=True)
                if data is None:
                    return 'Not a JSON', 400
                if 'name' not in data.keys():
                    return 'Missing name', 400
                for key in data:
                    if key not in ignored_keys:
                        setattr(cities, key, data[key])
                    setattr(cities, "state_id", state_id)
                cities.save()
                return cities.to_dict(), 201
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def cities_by_id(city_id):
    """ Handles GET, DELETE and PUT requests for cities by id """
    city_obj = storage.all(City)
    for key, val in city_obj.items():
        if val.id == city_id:

            if request.method == 'GET':
                return val.to_dict()

            if request.method == 'PUT':
                data = request.get_json(silent=True)
                if data is None:
                    return 'Not a JSON', 400
                for key in data:
                    if key not in ignored_keys:
                        setattr(val, key, data[key])
                storage.save()
                return val.to_dict(), 200

            if request.method == 'DELETE':
                storage.delete(val)
                storage.save()
                return {}, 200
    abort(404)