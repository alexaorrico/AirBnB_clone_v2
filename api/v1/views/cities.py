#!/usr/bin/python3
"""Flask route for city model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id=None):
    """route to return all cities"""

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == "GET":
        cities_dict = storage.all(City)
        cities_list = [obj.to_dict() for obj in cities_dict.values()
                       if obj.state_id == state_id]
        return jsonify(cities_list)

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("name") is None:
            abort(400, "Missing name")

        request_json["state_id"] = state_id
        newCity = City(**request_json)
        newCity.save()
        return make_response(jsonify(newCity.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def city(city_id=None):
    """Get, update or delete state with city id"""
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(city_obj.to_dict())

    if request.method == "DELETE":
        city_obj.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        city_obj.update(request_json)
        return make_response(jsonify(city_obj.to_dict()), 200)
