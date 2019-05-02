 #!/usr/bin/python
"""holds class City"""
from models.state import State
from models.city import City
from flask import abort
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv
from models import storage


@app_views.route("states/<state_id>/cities", strict_slashes=False, methods=['GET'])
def all_cities(state_id):
    """grab all cities in a state"""
    print(state_id)
    obj = [city.to_dict() for city in cities if city.state_id == state_id]
    print("here she is {}".format(obj))
    if len(obj) == 0:
        abort(404)
    return jsonify(obj)


@app_views.route("cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_obj(city_id):
    """retrieve city obj"""
    obj = [city.to_dict() for city in cities if city.id == city_id]
    if len(obj) == 0:
        abort(404)
    return jsonify(obj)


@app_views.route("cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete a city"""
    obj = storage.get("City", city_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """create new city obj"""
    data = request.get_json()
    if 'name' not in data.keys():
        abort 404
    try:
        json_obj = json.loads(data)
    except ValueError as e:
        abort 400
    new_city = City(state_id=state_id)
    cities = storage.all(City)
    for city in cities.values():
        if city.state_id == state_id:
            return new_city, 201
    abort 404
