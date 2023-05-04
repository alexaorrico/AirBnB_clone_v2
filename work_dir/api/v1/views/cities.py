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


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def Mypost(state_id):
    """
    Creates a neegrw instance of city
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missinng name"}), 400)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cityToPost = request.get_json()
    cityToPost['state_id'] = state_id

    city = City(**cityToPost)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a city instance"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    obj_dict = request.get_json()
    for key, value in obj_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
