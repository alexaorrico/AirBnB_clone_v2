#!/usr/bin/python3
'''module api/v1/views/cities.py:
create a new view for City objects - handles all default RESTful API actions
'''
from flask import abort, jsonify, request

from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    '''GET /states/<state_id>/cities
    Retrieves the list of all City objects of a State
    '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    '''GET /cities/<city_id>
    Retrieves a City object
    '''
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''DELETE /cities/<city_id>
    Deletes a City object
    '''
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''POST /states/<state_id>/cities
    creates a City object
    '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''PUT /cities/<city_id>
    updates a City object
    '''
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''404: Not Found'''
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''400:
    return Bad Request message for illegal requests to API
    '''
    return jsonify({'error': 'Bad Request'}), 400