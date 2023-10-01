#!/usr/bin/python3
"""
    module cities
"""

import models
from models import storage
from models.state import *
from models.city import *

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """
        A function that Retrieves the list of all City
        objects of a State: GET /api/v1/states/<state_id>/cities
    """
    # get state by id
    state = storage.get(State, state_id)

    # get cites in states and return
    if (state):
        stateCites = [city.to_dict() for city in state.cities]

        return jsonify(stateCites)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
        A function that Retrieves a City object:
        GET /api/v1/cities/<city_id>
    """
    # get city by id
    obj = storage.get(City, city_id)

    # return city is found
    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """
        A function that Deletes a City object:
        DELETE /api/v1/cities/<city_id>
    """
    # get city by id
    obj = storage.get(City, city_id)

    # is city is found, delete object, save and return {}
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_state(state_id):
    """
        A function that Creates a City:
        POST /api/v1/states/<state_id>/cities
    """
    json_str = request.get_json()
    state = storage.get(State, state_id)

    if (state):
        # Check If the HTTP body request is not valid JSON
        if (not json_str):
            abort(400, 'Not a JSON')
        if ('name' not in json_str):
            abort(400, 'Missing name')

        # save state id to json sting
        json_str['state_id'] = state_id
        # create city object
        obj = City(**json_str)
        obj.save()

        return jsonify(obj.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(city_id):
    """
        A function that Updates a City object:
        PUT /api/v1/cities/<city_id>
    """
    # get the city by id
    obj = storage.get(City, city_id)

    if (obj):
        json_str = request.get_json()
        # Check If the HTTP body request is not valid JSON
        if (not json_str):
            abort('400', 'Not a JSON')

        # Update City object attributes
        to_ignore = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in json_str.items():
            if key not in to_ignore:
                setattr(obj, key, value)

        #  save and return
        obj.save()

        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
