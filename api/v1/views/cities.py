#!/usr/bin/python3
""" Route Cities """
from flask import request, abort, jsonify
from api.v1.app import *
from api.v1.views.index import *
from models import storage, City


def validate(obj, ref_id):
    """ validate if query have id to reference """
    try:
        valid = storage.get(obj, ref_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def get_state_and_city(state_id, city_id):
    """ list of city objects filter by state """
    if (city_id is not None):
        get_city = validate(City, city_id).to_dict()
        return jsonify(get_city)
    state_obj = storage.get(State, state_id)
    try:
        state_cities = state_obj.cities
    except Exception:
        abort(404)
    cities = []
    for city in state_cities:
        cities.append(city.to_dict())
    return jsonify(cities)


def delete_city(id_city):
    """ delete city """
    city = validate(City, id_city)
    storage.delete(city)
    storage.save()
    response = {}
    return jsonify(response)


def create_city(request, state_id):
    """ create city """
    validate(State, state_id)
    request_json = request.get_json()
    if (request_json is None):
        abort(400, 'Not a JSON')
    try:
        name_city = request_json['name']
    except Exception:
        abort(400, "Missing name")
    city = City(name=name_city, state_id=state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict())


def update_city(city_id, request):
    """ updates city """
    get_city = validate(City, city_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for key, value in body_request.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(get_city, key, value)
    storage.save()
    return jsonify(get_city.to_dict())


@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'],
                 defaults={'city_id': None}, strict_slashes=False)
@app_views.route('/cities/<city_id>', defaults={'state_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def cities(state_id, city_id):
    """ Switch routes """
    if (request.method == "GET"):
        return get_state_and_city(state_id, city_id)
    elif (request.method == "DELETE"):
        return delete_city(city_id)
    elif (request.method == "POST"):
        return create_city(request, state_id), 201
    elif (request.method == "PUT"):
        return update_city(city_id, request), 200