#!/usr/bin/python3
""" Methos API for object citys """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_state_city(state_id):
    """ Get one Cites objects of State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """ Get one City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Delete a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Create a new City object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_city = request.get_json()
    if not request_city:
        abort(400, "Not a JSON")
    if "name" not in request_city:
        abort(400, "Missing name")
    city = City(**request_city)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ Update a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_city = request.get_json()
    if not request_city:
        abort(400, "Not a JSON")

    for key, value in request_city.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
