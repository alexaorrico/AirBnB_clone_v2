#!/usr/bin/python3
''' Creating cities flask app'''

from flask import Flask, jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def allCities(state_id):
    ''' gets all cities from a state'''

    states = storage.all(State)

    if 'State.' + str(state_id) not in states:
        abort(404)

    cities = storage.all(City)
    cityList = []

    for city in cities.values():
        if city.state_id == state_id:
            cityList.append(city.to_dict())
    return jsonify(cityList)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCityID(city_id):
    ''' gets the city id'''

    focusedCity = storage.get(City, city_id)

    if focusedCity is None:
        abort(404)

    return jsonify(focusedCity.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteCity(city_id):
    ''' deletes a city '''

    focusedCity = storage.get(City, city_id)

    if focusedCity is None:
        abort(404)

    storage.delete(focusedCity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def postCity(state_id):
    ''' creates a city from a given state '''

    if storage.get(State, state_id) is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    jsonReq = request.get_json()
    jsonReq['state_id'] = state_id

    if 'name' not in jsonReq:
        abort(400, description='Missing name')

    newCity = City(**jsonReq)

    storage.new(newCity)
    storage.save()

    return jsonify(newCity.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id):
    ''' updates a city with a given city id'''

    focusedCity = storage.get(City, city_id)

    if focusedCity is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    jsonReq = request.get_json()
    ignoreKeys = ['id', 'created_at', 'updated_at', 'state_id']

    for key, value in jsonReq.items():
        if key not in ignoreKeys:
            setattr(focusedCity, key, value)

    storage.save()

    return jsonify(focusedCity.to_dict()), 200
