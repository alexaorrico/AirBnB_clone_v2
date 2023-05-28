#!/usr/bin/python3
"""
handles all default RESTFul API actions for city class
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def retrieve_city_using_stateid(state_id):
    """
    Retrieves a city using the state id
    Raises a 404 error if the state id is not found
    """
    states = storage.get(State, state_id)
    cities_list = []
    if states:
        for state in states.cities:
            cities_list.append(state.to_dict())
        return jsonify(cities_list)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_city_using_cityid(city_id):
    """
    REtrieves a city using the city id
    if the city_id is not linked to any City object, raise a 404 error
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_using_cityid(city_id):
    """
    Deletes a city using the city id
    If the city_id is not linked to any City object, raise a 404 error
    """
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """
    uploads a new city
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    form = request.get_json()
    obj = City(**form)
    obj.state_id = state.id
    obj.save()
    return jsonify(state.to_dict())


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city_using_cityid(city_id):
    """
    updates a city
    """
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, "Not a JSON")
        update = request.get_json()
        keys_ignore = ["id", "created_at", "updated_at"]
        for key, value in update.items():
            if key not in keys_ignore:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
    abort(404)
