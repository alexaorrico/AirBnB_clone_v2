#!/usr/bin/python3
""" A new view that handles all default api actions to the City """
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ A route on the endpoint that returns all the cities in a state """
    all_states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    all_cities = storage.all(City).values()
    city_obj = [obj.to_dict() for obj in all_cities if
                obj.state_id == state_id]
    return jsonify(city_obj), 200


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_city_by_id(city_id):
    """ A route that retrieves the city based on the city id """
    all_cities = storage.all(City).values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    return jsonify(city_obj[0])


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """ A route that deletes a city based on the city id"""
    all_cities = storage.all(City).values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    city_obj.remove(city_obj[0])
    for obj in all_cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/', strict_slashes=False,
                 methods=['POST'])
def post_city_objects(state_id):
    """ A route that allows addition of cities to the storage"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    cities = []
    new = City(state_id=state_id, name=request.json['name'])
    storage.new(new)
    storage.save()
    cities.append(new.to_dict())
    return jsonify(cities[0]), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ A route to update a specific city based on the city id"""
    all_cities = storage.all(City).values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city_obj[0]['name'] = request.json['name']
    for obj in all_cities:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(city_obj[0]), 200
