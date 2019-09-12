#!/usr/bin/python3
'''Creates cities route and returns valid JSON'''
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import request, jsonify, make_response, abort


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def state_cities_route(state_id):
    '''Returns a JSON of a city object'''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        city_list = []
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)

    if request.method == 'POST':
        new_city = request.get_json()
        if not new_city:
            abort(400, 'Not a JSON')
        if "name" not in new_city:
            abort(400, 'Missing name')
        new_city['state_id'] = state_id
        new_city_obj = City(**new_city)
        new_city_obj.save()
        return jsonify(new_city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_route(city_id):
    '''Retrieves cities within the state object'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        '''GET retrieves from the db a specific city by id'''
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        '''DELETE removes from db the specific city object'''
        storage.delete(city)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        '''PUT updates the city object with name of the city changed'''
        city_put = request.get_json()
        if city_put is None:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in city_put.items():
            if key not in ignore_keys:
                setattr(city, key, value)
                city.save()
        return make_response(jsonify(city.to_dict()), 200)
