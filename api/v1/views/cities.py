#!/usr/bin/python3
""" Module for state object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Returns all cities objects of a certain list """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities_dict_list = [city.to_dict() for
                        city in storage.all("City").values() if
                        city.state_id == state_id]
    return jsonify(cities_dict_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """ Method retrieves city object with certain id """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Method deletes city object based off of its id """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Method creates new city object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get("name") is None:
        abort(400, "Missing name")
    city = City(**body)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ Method updates a city object based off its id """
    city = storage.get("City", city_id)
    body = request.get_json()
    if not city:
        abort(404)
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict())
