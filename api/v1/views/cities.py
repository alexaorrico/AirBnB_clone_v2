#!/usr/bin/python3
""" State/Cities """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_reponse, abort, request
from models import storage
from models.state import State
from models.city import City
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities', methods=['GET','POST'],
                 strict_slashes=False)
def all_state_cities(state_id):
    """ list all cities in state """
    output = []
    state = storage.get(State, state_id)
    if states is None:
        abort(404)
    if request.method == 'GET':
        for city in state.cities:
            output.append(city.to_dict())
        return (jsonify(output))
    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        data['state_id'] = state_id
        city = City(**data)
        city.save()
        return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/city_id', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        output = city.to_dict()
        return (jsonify(output))
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
    if request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(city, key, value)
        city.save()
        return (jsonify(city.to_dict()), 200)

