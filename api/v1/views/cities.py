#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from flask import jsonify
from flask import abort
from flask import request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities(state_id):
    """Retrieves the list of all City objects"""
    try:
        state = storage.get(State, state_id)
        CityList = []
        for city in state.cities:
            CityList.append(city.to_dict())
        return jsonify(CityList)
    except:
        abort(404)


@app_views.route("/cities/<string:city_id>", methods=['GET'])
def citiesGet(city_id):
    """Retrieves a City object"""
    try:
        cities = storage.get(City, city_id).to_dict()
        return jsonify(cities)
    except:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def citiesDel(city_id):
    """Deletes a City object"""
    try:
        storage.delete(City, city_id)
        storage.save()
        return {}, 200
    except:
        abort(404)


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], endpoint='CitysPost')
def citiesPost(state_id):
    """Creates a City"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    try:
        stat = storage.get(State, state_id)
    except:
        abort(404)
    instance = City(**data)
    instance.state_id = state_id
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def citiesPut(city_id):
    """Updates a City object"""
    k = "City." + str(city_id)
    if k not in storage.all():
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(storage.all()[k], key, value)
    storage.all()[k].save()
    return jsonify(storage.get(City, city_id).to_dict()), 200
