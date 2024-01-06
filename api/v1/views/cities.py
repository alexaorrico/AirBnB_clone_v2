#!/usr/bin/python3
""""view for City objects that handles all default RESTFul API actions"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def get_create_city(state_id):
    """create a city object or display all cities with state_id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if request.method == "GET":
        return jsonify([city.to_dict() for city in state.cities])
    return create_city(state_id)


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def get_delete_update_city(city_id):
    """retrieves, deletes or update a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    city_data = request.get_json(silent=True)
    if city_data is None:
        abort(400, "Not a JSON")

    ignore_attr = ["id", "updated_at", "created_at", "state_id"]
    [setattr(city, attr, city_data[attr])
     for attr in city_data if attr not in ignore_attr]

    return jsonify(city.to_dict())


def create_city(state_id):
    """"create a city object"""
    city_data = request.get_json(silent=True)

    if city_data is None:
        abort(400, "Not a JSON")
    if "name" not in city_data:
        abort(400, "Missing name")

    new_city = City(state_id=state_id, name=city_data["name"])
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)
