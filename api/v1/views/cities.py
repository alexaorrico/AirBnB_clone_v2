#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route("states/<state_id>/cities", methods=['GET', 'POST'])
def citys_without_id(state_id=None):
    """Create a new city or return all the cities"""
    city = storage.get(State, state_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        cities_list = []
        cities_dict = storage.all(City)
        for city in cities_dict.values():
            if city.state_id == state_id:
                cities_list.append(city.to_dict())
        return jsonify(cities_list), 200

    if request.method == 'POST':
        json = request.get_json(silent=True)
        if json is None:
            abort(400, "Not a JSON")
        if json.get('name') is None:
            abort(400, "Missing name")
        json['state_id'] = state_id
        city = City(**json)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route("cities/<city_id>", methods=['GET', 'PUT', 'DELETE'])
def citys_with_id(city_id=None):
    """Perform READ UPDATE DELETE operations on a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        del city
        return jsonify({}), 200

    if request.method == 'PUT':
        json = request.get_json(silent=True)
        if json is None:
            abort(400, "Not a JSON")
        city.update(**json)
        return jsonify(city.to_dict()), 200
