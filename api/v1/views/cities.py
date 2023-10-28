#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_state_cities(state_id):
    """return a list of cities in the state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    citi = state.cities
    if not citi:
        abort(404)
    else:
        return jsonify([cit.to_dict() for cit in citi])


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/city/get_id.yml", methods=["GET"])
def get_city_id(city_id):
    """Retrieves a specific city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/city/delete.yml", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a  city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
@swag_from("documentation/city/post_city.yml", methods=["POST"])
def post_city(state_id):
    """
    Creates a City object
    """
    if not storage.get(State, state_id):
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    body = request.get_json()
    instance = City(**body)
    instance.state_id = state_id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/city/put_city.yml", methods=["PUT"])
def put_city(city_id):
    """put city change the values of the city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in dict(request.get_json()).items():
        setattr(city, key, val)
    
    storage.save()

    return jsonify(city.to_dict())
