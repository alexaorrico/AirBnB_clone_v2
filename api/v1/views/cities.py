#!/usr/bin/python3
'''contains city routes'''
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def state_cities(state_id):
    '''fetches cities belonging to a state'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = [c.to_dict() for c in state.cities]
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''fetches city using id'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''deletes a city'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    '''creates a new city'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        data = request.get_json()
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        data['state_id'] = state.id
        city = City(**data)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    '''updates a city'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    city.name = data['name']
    city.save()
    return jsonify(city.to_dict()), 200
