#!/usr/bin/python3
'''
API module to create cities
'''
from models import storage
from models.state import State
from models.city import City
from flask import request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    '''
    finds all city objects and returns them
    '''
    all_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    """ else:
        for i in storage.all("State").values():
            all_cities.append(i.to_dict()) """

    cities = storage.all("City").values()
    for city in cities:
        if city.state_id == state_id:
            print(city.state_id)
            all_cities.append(city.to_dict())
            print(all_cities)
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_one_city(city_id):
    '''
    retrieves and outputs 1 city based on id
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''
    delectes 1 city based on id
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    '''
    posts a city
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    city_new = City(**state_id, **data)
    storage.new(city_new)
    storage.save()
    return jsonify(city_new.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    '''
    puts a city based on it's id
    '''
    city = storage.get("City", city_id)
    if city_id is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, "Not a JSON")
    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            new_info = {"name": city_id}
            data.update(new_info)
    storage.save()
    return jsonify(data), 200
