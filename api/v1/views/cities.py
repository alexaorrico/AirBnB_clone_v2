#!/usr/bin/python3
'''
    RESTful API for City object
'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_all_cities(state_id):
    """Retrieves the list of all City objects
     of a State: GET /api/v1/states/<state_id>/cities
    """
    try:
        city_state = []
        storage_list_state = storage.get('State', 'state_id')
        if not storage_list_state:
            abort(404)
        for value in storage_list_state.cities:
            city_state.append(value.to_dict())
        return jsonify(city_state)


@app_views.route('/states/<state_id>/cities', methods=['GET\
'], strict_slashes=False)
def displayCitiesByState(state_id):
    """Return the cities by state if not error 404
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    lista = []
    for i in state.cities:
        lista.append(i.to_dict())
    return jsonify(lista)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def displayCities(city_id):
    """Return the cities if not error 404
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteCity(city_id):
    """Delete a city if not error 404
    """
    list_cities = {}
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST\
'], strict_slashes=False)
def createCity(state_id):
    """Create a city if not error 404
    """
    flag_state_id = 0
    city = request.get_json()
    if not city:
        abort(400, {'Not a JSON'})
    if 'name' not in city:
        abort(400, {'Missing name'})
    states = storage.all('State')
    text_final = "{}.{}".format('State', state_id)
    for key, value in states.items():
        if key == text_final:
            flag_state_id = 1
            break
    if flag_state_id == 0:
        abort(404)
    city.update(state_id=state_id)
    new_city = City(**city)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id):
    """Update a city if not error 404
    """
    city = request.get_json()
    if not city:
        abort(400, {'Not a JSON'})
    cities = storage.get('City', city_id)
    if not cities:
        abort(404)
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in city.items():
        if key not in ignore:
            setattr(cities, key, value)
    storage.save()
    return jsonify(cities.to_dict()), 200
