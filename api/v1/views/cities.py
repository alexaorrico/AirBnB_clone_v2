#!/usr/bin/python3
"""state JSON"""
from flask import abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from json import dumps


def json_ser(obj):
    json_obj = {}
    for key in obj:
        json_obj[key] = obj[key].to_dict()
    return (json_obj)


def cities_json(lst):
    json_list = []
    for city in lst:
        json_list.append(city.to_dict())
    return (json_list)


@app_views.route('/states/<state_id>/cities')
def citiesInState(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        return abort(404)
    return make_response(
        dumps(cities_json(obj.cities)),
        200)


@app_views.route('/cities/<city_id>')
def city_getter(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        return abort(404)
    return make_response(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        return abort(404)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_post(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    try:
        data = request.get_json()
        if 'name' not in data:
            return abort(400, description='Missing name')
        data['state_id'] = state_id
        new_city = City(**data)
        storage.new(new_city)
        storage.save()
        return make_response(new_city.to_dict(), 201)
    except Exception:
        return abort(400, description="Not a JSON")


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_put(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    try:
        data = request.get_json()
        for key in data:
            if key in ['id', 'state_id', 'created_at', 'updated_at']:
                continue
            value = data[key]
            if hasattr(city, key):
                try:
                    value = type(getattr(city, key))(value)
                except ValueError:
                    pass
            setattr(city, key, value)
        storage.save()
        return make_response(city.to_dict(), 200)
    except Exception:
        return abort(400, description="Not a JSON")
