#!/usr/bin/python3
"""
Task 8
Create a new view for City objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    all_cities = []
    if not storage.get('State', state_id):
        abort(404)
    for city in storage.all('City').values():
        if state_id == city.to_dict()['state_id']:
            all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_city(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/api/v1/states/<state_id>/cities', methods=['PUT'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
    city_list = request.get_json()
    if not storage.get('State', state_id):
        abort(404)
    if not city_list:
        abort(400, {'Not a JSON'})
    elif 'name' not in city_list:
        abort(400, {'Missing name'})
    city_list['state_id'] = state_id
    new_city = City(**city_list)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>', methods=['POST'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    update_obj = request.get_json()
    if not update_obj:
        abort(400, {'Not a JSON'})
    this_city = storage.get('City', city_id)
    if not this_city:
        abort(404)
    for key, value in update_obj.items():
        setattr(this_city, key, value)
    storage.save()
    return jsonify(this_city.to_dict()), 200
