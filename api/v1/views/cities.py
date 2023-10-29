#!/usr/bin/python3
'''This module Retrieves the list of all City objects,
deletes, updates, creates and gets information of a city '''

from flask import jsonify, request, abort
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_all_cities(state_id):
    ''' retreive all city associted with the state obj'''
    state_objs = storage.all('State')
    key = 'State.{}'.format(state_id)

    if key in state_objs:
        state = state_objs.get(key)
        return jsonify([obj.to_dict() for obj in state.cities])

    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_a_cities(city_id):
    '''return the city with matching id'''
    city_objs = storage.all('City')
    key = 'City.{}'.format(city_id)

    if key in city_objs:
        city = city_objs.get(key)
        return jsonify(city.to_dict())

    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_cities(city_id):
    ''' delete a city matching the id'''
    city_objs = storage.all('City')
    key = 'City.{}'.format(city_id)

    if key in city_objs:
        obj = city_objs.get(key)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_a_cities(state_id):
    ''' create a city '''

    data = request.get_json()
    state_objs = storage.all('State')
    key = 'State.{}'.format(state_id)

    if key not in state_objs:
        abort(404)

    if data is None:
        abort(400, "Not a JSON")
    if data.get('name') is None:
        abort(400, "Missing name")

    data["state_id"] = state_id
    city_obj = City(**data)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_a_cities(city_id):
    ''' update a city '''

    data = request.get_json()
    city_objs = storage.all('City')
    key = 'City.{}'.format(city_id)

    if key not in city_objs:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")

    city = city_objs.get(key)
    for k, v in data.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
