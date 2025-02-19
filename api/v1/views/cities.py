#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities")
def get_cities(state_id):
    """get all cities belong state"""
    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    else:
        cities = []
        for city in res.cities:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>")
def get_city(city_id):
    """get city"""
    res = storage.get(City, city_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """add new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.json is None:
        abort(400, "Not a JSON")
    data = request.get_json()
    if data.get('name') is None:
        return "Missing name", 400
    data["state_id"] = state_id
    new_city = City(name=request.json['name'], state_id=state.id)
    # new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if request.json is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
