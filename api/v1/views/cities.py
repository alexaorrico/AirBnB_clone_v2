#!/usr/bin/python3
"""
this module creates a new view for City objects
that handles all default RESTFul API actions
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def getCityByState(state_id):
    """
    returns all cities in a state
    """
    if 'State.{}'.format(state_id) in storage.all():
        dict_cities = storage.all(City)
        cities_by_state = [v.to_dict() for v in dict_cities.
                           values() if v.state_id == state_id]
        return jsonify(cities_by_state), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def getCityById(city_id):
    """
    returns a city by its id
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def deleteCity(city_id):
    """
    deletes a city
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def createCity(state_id):
    """
    creates a city
    """
    if 'State.{}'.format(state_id) in storage.all():
        if request.is_json:
            request_data = request.get_json()
            if 'name' in request_data:
                name = request_data['name']
                newCity = City(state_id=state_id, name=name)
                newCity.save()
                newCityDict = storage.get(City, newCity.id).to_dict()
                return jsonify(newCityDict), 201
            else:
                return jsonify(message='Missing name'), 400
        else:
            return jsonify(message='Not a JSON'), 400
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def updateCity(city_id):
    """
    updates city
    """
    city = storage.get(City, city_id)
    if city:
        forbidden_keys = ['id', 'state_id', 'created_at', 'updated_at']
        if request.is_json:
            argsDict = request.args
            argsDict = request.get_json()
            for k, v in argsDict.items():
                if k not in forbidden_keys:
                    setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict()), 200
        else:
            return jsonify(message='Not a JSON'), 400
    else:
        abort(404)
