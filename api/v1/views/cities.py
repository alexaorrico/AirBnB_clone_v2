#!/usr/bin/python3
"""view of City objects"""
from api.v1.views import app_views
from models import storage, city
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=["GET"])
def return_cities(state_id):
    """return json City objects"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = []
    for city in storage.all('City').values():
        if city.state_id == state.id:
            cities.append(city.to_dict())
    if len(cities) == 0:
        abort(404)
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=["GET"])
def return_city(city_id):
    """return a city"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=["POST"])
def add_city(state_id):
    """add a city to a state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, message="Not a JSON")
    if 'name' not in data.keys():
        abort(400, message="Missing name")
    new_city = city.City(state_id=state.id)
    for k, v in data.items():
        setattr(new_city, k, v)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """update a city"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, message="Not a JSON")
    checker = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in checker:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
