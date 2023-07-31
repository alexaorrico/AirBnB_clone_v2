#!/usr/bin/python3
""" View for City objects that handles all default RESTFul API actions """
from . import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_cities_in_state(state_id=None):
    states_ = storage.get('State', state_id)

    if states_ is None:
        abort(404, 'Not found')

    cities_dict = storage.all('City')
    state_cities = ([obj.to_json()
                    for obj in cities_dict.values()
                    if obj.state_id == state_id])
    return jsonify(state_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city by its id"""
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404, "Not Found")
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """ Deletes a city."""
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False,
    )
def post_city(state_id):
    """ Creates a City """
    data = request.get_json()
    states_ = storage.get('State', state_id)

    if states_ is None:
        abort(404, 'Not found')

    if not data:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    data["state_id"] = state_id
    city_obj = City(**data)
    city_obj.save()
    return make_response(jsonify(city_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_state(city_id):
    """ Updates a City object"""
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)
    city_obj.save()
    return make_response(jsonify(city_obj.to_dict()), 200)
