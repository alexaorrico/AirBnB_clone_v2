#!/usr/bin/python3
"""view for city object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_state(state_id):
    """Returns a list of all city objects of a state"""
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Return a dict representation of city object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a city object"""
    state = storage.get(State, state_id)
    if state:
        if request.get_json():
            if 'name' in request.get_json():
                data = request.get_json()
                data['state_id'] = state_id
                city = City(**data)
                city.save()
                return city.to_dict(), 201
            else:
                return abort(400, "Missing name")
        else:
            return abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """updates city object"""
    city = storage.get(City, city_id)
    if city:
        if request.get_json():
            for key, value in request.get_json().items():
                if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                    setattr(city, key, value)
            city.save()
            return city.to_dict(), 200
        else:
            return abort(400, "Not a JSON")
    else:
        abort(404)
