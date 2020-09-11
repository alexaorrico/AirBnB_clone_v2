#!/usr/bin/python3
""" City view """
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views, State, City
from flask import abort


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Retrives the list of all City objs base on state_id """
    objs = storage.get(State, state_id)
    _cities = []
    if objs.__class__.__name__ == 'State':
        for city in objs.cities:
            _cities.append(city.to_dict())
        return jsonify(_cities)
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities_by_id(city_id):
    """ Retrieves City objects """
    city = storage.get(City, city_id)
    result = None
    if city.__class__.__name__ == 'City':
        result = jsonify(city.to_dict())
    else:
        result = abort(404)
    return result


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """ DELETE city by ID """
    city_object = storage.get(City, city_id)
    result = None
    if city_object.__class__.__name__ == 'City':
        storage.delete(city_object)
        storage.save()
        result = make_response(jsonify({}), 200)
    else:
        result = abort(404)
    return result


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """ Creates a City obj """
    state_object = storage.get(State, state_id)
    if not state_object.__class__.__name__ == 'State':
        return abort(404)
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            result = jsonify({'error': 'Missing name'}), 400
        else:
            new_object = City(**data)
            setattr(new_object, 'state_id', state_id)
            storage.new(new_object)
            storage.save()
            result = jsonify(new_object.to_dict()), 201
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    """ PUT cities """
    city_object = storage.get(City, city_id)
    if not city_object.__class__.__name__ == 'City':
        return abort(404)
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(city_object, key, value)
        storage.save()
        result = jsonify(city_object.to_dict()), 200
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result
