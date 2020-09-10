#!/usr/bin/python3
"""Create a new view for State objects"""

from flask import jsonify, request, abort
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_list(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        cities = storage.all("City")
        cities_list = []
        for city in cities.values():
            if city.state_id == state_id:
                cities_list.append(city.to_dict())
        return jsonify(cities_list)
    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if "name" not in response:
            abort(400, "Missing name")
        response["state_id"] = state_id
        new_city = City(**response)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_id(city_id):
    """Manipulate a specific City object:"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
