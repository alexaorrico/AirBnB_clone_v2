#!/usr/bin/python3
''' This module defines a view for City objects '''
from api.v1.views import state_views
from api.v1.views import city_views
from models import storage
from models.state import State
from models.city import City
from flask import request, abort
import json


@city_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    ''' Retrieves a list of cities of a state '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return json.dumps(cities, indent=4)


@city_views.route('/cities/<city_id>')
def get_city(city_id):
    ''' Retrieves a city object '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return json.dumps(city.to_dict(), indent=4)


@city_views.route('/cities/<city_id>', methods=['DELETE'],
                  strict_slashes=False)
def delete_city(city_id):
    ''' Deletes a city '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()

    return json.dumps({}, indent=4), 200


@city_views.route('/states/<state_id>/cities', methods=['POST'],
                  strict_slashes=False)
def post_city():
    ''' Creates a city '''
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        if 'name' not in data:
            abort(400, description='Missing name')
        city = City(**data)
        city.save()
        return json.dumps(city.to_dict(), indent=4), 201


@city_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    ''' Updates a city '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(city, key, value)
            city.save()
            return json.dumps(city.to_dict(), indent=4), 200
