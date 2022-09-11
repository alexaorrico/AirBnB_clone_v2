#!/usr/bin/python3
"""adasda"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getCity(state_id):
    """aaasdasdasd"""
    ciudades = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for ciudad in state.cities:
        ciudades.append(ciudad.to_dict())
    return jsonify(ciudades)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCityById(city_id):
    """asdasdasda"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id):
    """asdasdasda"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def CreateCity(state_id):
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    if json_req.get("name") is None:
        abort(400, 'Missing name')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_obj = City(**json_req)
    new_obj.state_id = state_id
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def updateCity(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    for key, value in json_req.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
