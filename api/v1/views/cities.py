#!/usr/bin/python3
""" this script create a new view for City object """


from models.city import City
from models import storage
from flask import Flask, abort, jsonify, request, json
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_of_a_state(state_id):
    """ serializate an object into a valid JSON """
    cities = []
    for state_key, value_state in storage.all("State").items():
        if state_id == value_state.id:
            for key, value in storage.all("City").items():
                if state_id == value.state_id:
                    cities.append(value.to_dict())
    if storage.get("State", state_id):
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """ retrieves a object with id """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """ delete a object by id """
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_a_city(state_id):
    """ create a city """
    if request.is_json:
        dicc = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" in dicc:
        new_city = City()
        new_city.name = dicc["name"]
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    else:
        return jsonify({"error": "Missing name"}), 400


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_a_city(city_id):
    """update a cities """
    if not request.json:
        abort(400, "Not a JSON")
    city = storage.get("City", city_id)
    if city:
        city.name = request.json['name']
        city.save()
        return jsonify(city.to_dict()), 200
    abort(404)
