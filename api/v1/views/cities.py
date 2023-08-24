#!/usr/bin/python3
"""cities view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_from_state_id(state_id):
    """returns all cities of state or 404"""
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cities_list = []
        for city, city_details in storage.all(City).items():
            city = city_details.to_dict()
            if city['state_id'] == str(state_id):
                cities_list.append(city)
        if cities_list is not None:
          return jsonify(cities_list)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_from_id(city_id):
    """returns city from id"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())

            
