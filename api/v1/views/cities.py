#!/usr/bin/python3
"""route /cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_from_state(state_id):
    """Method that retrieve a list of all cities by id"""
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)

    all_cities = [city.to_dict() for city in state.cities]

    return (jsonify(all_cities))


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_name(city_id=None):
    """ display a city object by name"""

    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404)

    return jsonify(city_object.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Method that delete a city by id"""
    delete_city = storage.get(City, city_id)
    if delete_city is None:
        abort(404)
    else:
        delete_city.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    ''' Create a State object '''
    post_city = request.get_json()
    if post_city is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if 'name' not in post_city:
        return (jsonify({'error': 'Missing name'}), 400)

    if (type(post_city) is dict):
        post_city['state_id'] = state_id
        obj = City(**post_city)

        storage.new(obj)
        storage.save()

        return (jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_cities_id(city_id):
    ''' Update a State object '''
    update_city = request.get_json()
    if update_city is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        ignore_key = ['id', 'state_at', 'created_at' 'updated_at']
        for key, value in update_city.items():
            if key not in ignore_key:
                setattr(city, key, value)
            else:
                pass
        storage.save()
        return (jsonify(city.to_dict()), 200)
