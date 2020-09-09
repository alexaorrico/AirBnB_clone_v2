#!/usr/bin/python3
"""
view for City objects that handles all default RestFul API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
# we import the Blueprint 'app_views'created in the __init__
from api.v1.views import app_views
from models.city import City


# the followings are the entendpoints of the app_view blueprint
# in other words /status == /api/v1/status and /stats == /api/v1/stats
# we create that blueprint to access to all the endpoints easily

@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities():
    """
    function to return the all City objects
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    all_cities = []
    cities = storage.all("City").values()
    for city in cities:
        if city.state_id == state_id:
            all_cities.append(city.to_json())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """
    function to return City object by id throught a GET method
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404, description="city_id not linked to any City object")
    city = city.to_json()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    function to delete City object by id throught a DELETE method
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404, description="city_id not linked to any City object")
    city.delete()
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    function to create a new City object throught a POST method
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    dic_json = request.get_json()
    if not dic_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in dic_json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_city = City(**dic_json)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    function to update a City object by id throught a PUT method
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404, description="city_id not linked to any City object")
    dic_json = request.get_json()
    if not dic_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            city.bm_update(key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
