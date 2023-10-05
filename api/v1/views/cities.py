#!/usr/bin/python3
"""
new view for City objects that handles all default
RESTFul API actions:
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False
                 )
def list_cities(state_id):
    """List all City objects"""
    states_dict = storage.all(State)
    cities_list = None
    return_list = []
    for state in states_dict.values():
        if state.id == state_id:
            cities_list = state.cities
    if cities_list is None:
        abort(404)
    for city in cities_list:
        return_list.append(city.to_dict())
    return jsonify(return_list)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False
                 )
def get_city(city_id):
    """Retrieves a `City` object."""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False
                 )
def delete_city(city_id):
    """Deletes a `City` object."""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False
                 )
def create_city(state_id):
    """Creates a `City` object."""
    try:
        request_dict = request.get_json(silent=True)
        if request_dict is not None:
            if 'name' in request_dict.keys()\
             and request_dict['name'] is not None:
                request_dict['state_id'] = state_id
                new_city = City(**request_dict)
                new_city.save()
                return make_response(jsonify(new_city.to_dict()), 201)
            return make_response(jsonify({'error': 'Missing name'}), 400)
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False
                 )
def update_city(city_id):
    """Updates a `City` object."""
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)