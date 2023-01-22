#!/usr/bin/python3
""" Endpoints for city related
    interactions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def city_by_state(state_id):
    """search for a state with given id and:
       return all list of its cities
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        if 'name' not in data.keys():
            return make_response('Missing name\n', 400)
        data.update({'state_id': state_id})
        new_city = City(**data)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def city_by_id(city_id):
    """search for a city with given id and:
        1. return it
        2. update it
        3. delete it
       depending on the method
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)


def get_json(request):
    """check if body has json data
       and handles errors reponses
    """
    #  exception handling to avoid calling
    #  on_json_loading_failed()
    try:
        data = request.get_json()
    except Exception:
        data = None
    return data
