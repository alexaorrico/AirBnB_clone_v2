#!/usr/bin/python3
""" Retrieves  api for cities"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flasgger.utils import swag_from


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities(state_id):
    """ module to get cities in states"""

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    cities = state.cities
    city_list = []

    for city in cities:
        city_list.append(city.to_dict())

    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """retrieves a city object"""

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """deletes a city"""

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def post_city(state_id):
    """creates a new city"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    info = request.get_json()
    new_city = City(**info)
    new_city.state_id = state_id
    new_city.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """Update a City"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
