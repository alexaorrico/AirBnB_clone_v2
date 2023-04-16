#!/usr/bin/python3
""" city view model"""
from models.city import City
from models.state import State
from flask import jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/', methods=['GET', 'POST'], defaults={'id': None})
@app_views.route('/cities/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def cities_view(id=None):
    """ city view model"""
    if id is not None:
        my_cities = storage.all(City)
        key = '{}.{}'.format(City.__name__, id)
        if key not in my_cities.keys():
            return jsonify(error='Not found'), 404
        city = my_cities[key]
        if request.method == "GET":
            return jsonify(city.to_dict())
        elif request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            update_values = request.get_json()
            if type(update_values) is not dict:
                return jsonify(error='Not a JSON'), 400
            for key, val in update_values.items():
                ls = ['id', 'created_at', 'updated_at']
                if key not in ls:
                    setattr(city, key, val)
            storage.save()
            return jsonify(city.to_dict())
    else:
        if request.method == 'GET':
            my_cities = storage.all(City)
            json_cities = []
            for city in my_cities.values():
                json_cities.append(city.to_dict())
            return jsonify(json_cities)


@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'])
def cities_by_state(state_id):
    """ city view model"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify(error='No state found'), 404
    if request.method == "GET":
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities), 200
    elif request.method == 'POST':
        update_values = request.get_json()
        if type(update_values) is not dict:
            return jsonify(error='Not a JSON'), 400
        if 'name' not in update_values.keys():
            return jsonify(error='Missing user_id'), 400
        x = City(name=update_values['name'], state_id=state_id)
        return jsonify(x.to_dict()), 201
