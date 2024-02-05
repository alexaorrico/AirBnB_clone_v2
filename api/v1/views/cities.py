#!/usr/bin/python3
'''Includes the cities view for the API.'''
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, storage_t
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_or_create_cities(state_id):
    """Retrieve list of all City objects of State or creates a new one"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        city = City(name=data['name'], state_id=state_id)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def get_update_or_delete_city(city_id):
    """Retrieves, updates or deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
