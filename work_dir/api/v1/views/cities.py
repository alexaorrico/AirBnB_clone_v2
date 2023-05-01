#!/usr/bin/python3
"""
This module will help us control and manage state objects using Restful api
"""
from flask import request, abort, jsonify, make_response
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def allCities_inState(state_id):
    """
    returns a list of all cities in a city
    """
    c_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        c_list.append(city.to_dict())
    return jsonify(c_list)


@app_views.route(
        "/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_a_city(city_id):
    """returns a single state"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route(
        "/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city_object(city_id):
    """
    delete a city object from the list
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_view.route(
        '/states/<state_id>/cities', method=['POST'], strict_slashes=False)
def Mypost(state_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}). 400)
