#!/usr/bin/python3
"""States views"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_get(state_id):
    """Retrieves the list of all City objects of a State"""
    all_state = storage.all()
    state_id = 'State.' + state_id
    all_cities = []
    if state_id in all_state.keys():
        for city in all_state[state_id].cities:
            all_cities.append(city.to_dict())
        return jsonify(all_cities)
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_cities(city_id):
    """Retrieves a City object"""
    all_city = storage.all(City)
    id_city = 'City.' + city_id
    if id_city in all_city.keys():
        return jsonify(all_city[id_city].to_dict())
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_cities(city_id):
    """Deletes a City object"""
    all_city = storage.all('City')
    id_city = 'City.' + city_id
    if id_city in all_city:
        storage.delete(all_city[id_city])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id):
    """Creates a City object"""
    all_state = storage.get('State', state_id)
    if all_state is None:
        abort(404)
    new_city = request.get_json()
    if new_city is None:
        abort(400, "Not a JSON")
    if 'name' not in new_city:
        abort(400, "Missing name")
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    """Updates a City object"""
    req = request.get_json()
    if not request.json:
        abort(400, "Not a JSON")
    city_to_modify = storage.get('City', city_id)
    if city_to_modify is None:
        abort(404)
    for key in req:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_to_modify, key, req[key])
    storage.save()
    return jsonify(city_to_modify.to_dict()), 200
