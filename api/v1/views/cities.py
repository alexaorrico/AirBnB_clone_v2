#!/usr/bin/python3
'''All city routes'''

from models import storage, City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_of_a_state(state_id):
    '''
        GET: Lists all cities in a specific state
        POST: Adds a city to a specific state
    '''
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    if request.method == 'POST':
        city_dict = request.get_json()
        if city_dict is None:
            return 'Not a JSON', 400
        if 'name' not in city_dict.keys():
            return 'Missing name', 400
        city_dict['state_id'] = state_id
        my_city = City(**city_dict)
        my_city.save()
        return jsonify(my_city.to_dict()), 201
    my_cities = [city.to_dict() for city in storage.all('City').values()
                 if city.state_id == state_id]
    return jsonify(my_cities)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_city(city_id):
    '''
        GET: display a specific city
        DELETE: delete a city
        PUT: update a city
    '''
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(my_city)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        city_dict = request.get_json()
        if city_dict is None:
            return 'Not a JSON', 400
        for key, value in city_dict.items():
            if key not in ['id', 'created_at', 'updated_at', 'state_id']:
                setattr(my_city, key, value)
        my_city.save()
    return jsonify(my_city.to_dict())
