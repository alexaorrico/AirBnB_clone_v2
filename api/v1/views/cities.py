#!/usr/bin/python3
"""
contains endpoints(routes) for states objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [obj.to_dict() for obj in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@ app_views.route("/cities/<string:city_id>", strict_slashes=False,
                  methods=['DELETE'])
def del_city(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@ app_views.route("/states/<string:state_id>/cities", strict_slashes=False,
                  methods=['POST'])
def create_city(state_id):
    """
    Creates a City instance
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    valid_json = request.get_json()

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in valid_json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj = City(**valid_json)
    obj.state_id = state.id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@ app_views.route("/cities/<string:city_id>", strict_slashes=False,
                  methods=['PUT'])
def update_city(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    valid_json = request.get_json()

    if not city:
        abort(404)

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in valid_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
