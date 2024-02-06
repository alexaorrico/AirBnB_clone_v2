#!/usr/bin/python3
"""
Define route for view City
"""
from api.v1.views import app_views
from flask import jsonify, abort, request 
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def city_state(state_id=None):
    """Retrieves and Creates a City given state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        elif 'name' not in data:
            abort(400, 'Missing name')
        else:
            data['state_id'] = state_id
            city = City(**data)
            city.save()
            return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city(city_id=None):
    """Retrieves, Delete and Update a City given city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
