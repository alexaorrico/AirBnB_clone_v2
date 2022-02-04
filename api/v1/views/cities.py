#!/usr/bin/python3
'''Contains the cities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_cities(state_id=None, city_id=None):
    '''The method handler for the cities endpoint.
    '''
    handlers = {
        'GET': get_cities,
        'DELETE': remove_city,
        'POST': add_city,
        'PUT': update_city,
    }
    if request.method in handlers:
        return handlers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_cities(state_id=None, city_id=None):
    '''Gets the city with the given id or all cities in
    the state with the given id.
    '''
    if state_id:
        state = storage.get(State, state_id)
        if state:
            all_cities = state.cities
            all_cities = list(map(lambda x: x.to_dict(), all_cities))
            return jsonify(all_cities)
    elif city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
    raise NotFound()


def remove_city(state_id=None, city_id=None):
    '''Removes a city with the given id.
    '''
    if city_id:
        city = storage.get(City, city_id)
        if city:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_city(state_id=None, city_id=None):
    '''Adds a new city.
    '''
    state = storage.get(State, state_id)
    if not state:
        raise NotFound()
    data = request.get_json()
    if data is None or type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    setattr(data, 'state_id', state_id)
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


def update_city(state_id=None, city_id=None):
    '''Updates the city with the given id.
    '''
    xkeys = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        old_city = storage.get(City, city_id)
        if old_city:
            data = request.get_json()
            if data is None or type(data) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in data.items():
                if key not in xkeys:
                    setattr(old_city, key, value)
            old_city.save()
            return jsonify(old_city.to_dict()), 200
    raise NotFound()
