#!/usr/bin/python3
""" citie module """


from flask import make_response, jsonify, request
from api.v1.views import api_views
import json
from models import storage
from models.city import City


@app.views.route('/states/<state_id>/cities')
def city_index(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return j.dumps(list(city, city.to_dict(),
                                state.cities))
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.views.route('/cities/<city_id>')
def get_city(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            return json.dumps(city.to_dict)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)
