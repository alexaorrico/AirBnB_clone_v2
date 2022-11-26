#!/usr/bin/python3
"""City bjects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all City objects """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """ Retrieves a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """ Creates a City object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    new_city_data = request.get_json()
    if not new_city_data:
        abort(400, "Not a JSON")
    if "name" not in new_city_data:
        abort(400, "Missing name")
    city = City(**new_city_data)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Updates a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
