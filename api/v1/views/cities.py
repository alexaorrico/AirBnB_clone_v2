#!/usr/bin/python3
""" Import the app_views blueprint for cities API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>/cities/', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ Get all cities objects """
    all_status = storage.all("State").values()
    state_objs = [state.to_dict() for state in all_status if state_id == state.id]
    if not state_objs:
        abort(404)
    all_cities = storage.all("City").values()
    list_cities = [city.to_dict() for city in all_cities if state_id == city.state_id]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Get a city by id """
    all_cities = storage.all("City").values()
    list_city = [city.to_dict() for city in all_cities if city.id == city_id]
    if not list_city:
        abort(404)
    return jsonify(list_city[0])


@app_views.route('/cities/<city_id>/', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ remove a city by id """
    all_cities = storage.all("City").values()
    list_city = [city.to_dict() for city in all_cities if city.id == city_id]
    if not list_city:
        abort(404)
    list_city.remove(list_city[0])
    for city in all_cities:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
@app_views.route('/api/v1/states/<state_id>/cities/', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ create a new city """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing nam'}), 400)
    all_states = storage.all("State").values()
    state = [state.to_dict() for state in all_states if state_id == state_id]
    if not state:
        abort(404)
    cities = []
    new_city = City(name=request.json["name"], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dict())
    return jsonify(cities[0]), 201