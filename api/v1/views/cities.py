#!/usr/bin/python3
'''
create a new view for City
objects that handles all default RESTFul API actions
'''

from flask import abort, jsonify, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    '''Retrieves the list of all City objects of a State'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''Retrieves a City object'''
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Deletes a City object'''
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
    '''Creates city object'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    if not request.get_json():
        abort(400, 'Not a JSON')
    
    jsonData = request.get_json()
    if 'name' not in jsonData:
        abort(400, 'Missing name')
    
    jsonData['state_id'] = state_id
    city = City(**jsonData)
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    '''Updates City Object'''
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')
        jsonData = request.get_json()
        ignoreKeys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in jsonData.items():
            if key not in ignoreKeys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    '''404 error'''
    return jsonify({'error': 'Not found'}), 404

@app_views.errorhandler(400)
def bad_request(error):
    '''Bad request error message'''
    return jsonify({'error': 'Bad Request'}), 400
