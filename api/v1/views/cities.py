#!/usr/bin/python3
""" Cities view """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """ Returns a list of all the cities in a given state """
    if not storage.get("State", state_id):
        abort(404)

    cities = []
    for city in storage.get("State", state_id).cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """ Returns a city specified by id """
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city specified by id """
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"], strict_slashes=False)
def add_city(state_id):
    """ Creates a city for a particular state """
    if not storage.get("State", state_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    city = City()
    city.name = request.get_json().get('name')
    city.state_id = state_id
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a city specified by id """
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, value in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at" \
           or key == "state_id":
            continue
        else:
            setattr(city, key, value)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
