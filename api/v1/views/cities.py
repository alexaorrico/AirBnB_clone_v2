#!/usr/bin/python3
"""
Define route for view City
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=['GET', 'PUT'])
def city_state(state_id=None):
    """Retrieves and Creates a City given state_id"""
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    elif request.method == 'PUT':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'not a json'}), 400)

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(City, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'POST'])
def city(city_id=None):
    if request.method == 'GET':

        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        else:
            city = City(**data)
            city.save()
            return make_response(jsonify(city.to_dict()), 201)
