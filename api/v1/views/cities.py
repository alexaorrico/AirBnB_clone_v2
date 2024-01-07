#!/usr/bin/python3
""" Cities routes for the API"""
from api.v1.views import app_views
from models import storage
from models.city import City
from flask import abort, jsonify, request

app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_cities(state_id):
    """Gets all the cities for a given state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        all_cities = storage.all('City')
        cities = [city.to_dict() for city in all_cities.values() 
                  if city.state_id == state_id]
        return jsonify(cities)

    if request.method  == 'POST':
        data =  request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        city = City(**data)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201


app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT', 'POST'])
def method_city(city_id):
    """Method for cities"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200