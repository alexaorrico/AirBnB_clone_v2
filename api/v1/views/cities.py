#!/usr/bin/python3
""" new view for State objects """

from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import Flask, make_response, jsonify
import requests
from flask import request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """ Retrieves the list of all State objects """
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    cities_objs = [city.to_dict() for city in storage.all(City).values()
                   if city.state_id == state_id]
    return make_response(jsonify(cities_objs), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    obj = storage.get(City, city_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """ Method DELETE """
    obj = storage.get(City, city_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    data = request.get_json(silent=True, force=True)
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)

    objs = City(**data)
    objs.state_id = state_id
    objs.save()
    return make_response(jsonify(objs.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    if city_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        obj = storage.get(City, city_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            data = request.get_json(silent=True, force=True)
            if data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(obj, item, value) for item, value in data.items()
             if item != ('id', 'created_at', 'updated_at', 'state_id')]
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
