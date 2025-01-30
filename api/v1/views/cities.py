#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getCities(state_id):
    """retrieves the list of all City objects of a State"""
    city_list = []
    state_ids = []
    all_states = storage.all(State)
    all_cities = storage.all(City)
    for val in all_states.values():
        state_ids.append(val.id)
    if state_id not in state_ids:
        return make_response({"error": "Not found"}, 404)
    for val in all_cities.values():
        if state_id == val.state_id:
            city_list.append(val.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>')
def getCity(city_id):
    """retrieve a City object"""
    all_cities = storage.all(City)
    for key, val in all_cities.items():
        if val.id == city_id:
            return jsonify(val.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id):
    """delete a City object"""
    all_cities = storage.all(City)
    for key, val in all_cities.items():
        if city_id == val.id:
            storage.delete(val)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createCity(state_id):
    """create a City object"""
    from models.city import City
    from models.state import State
    try:
        data = request.get_json()
        if "name" not in data:
            return make_response("Missing name", 400)
    except Exception as e:
        return make_response("Not a JSON", 400)
    all_states = storage.all(State)
    state_ids = []
    for val in all_states.values():
        state_ids.append(val.id)
    if state_id not in state_ids:
        return make_response({"error": "Not found"}, 404)
    new_city = City()
    data['state_id'] = state_id
    for key, value in data.items():
        setattr(new_city, key, value)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id):
    """update a City object"""
    all_cities = storage.all(City)
    try:
        data = request.get_json()
        for val in all_cities.values():
            if city_id == val.id:
                for key, value in data.items():
                    setattr(val, key, value)
                    storage.save()
                    return make_response(val.to_dict(), 200)
        return make_response({"error": "Not found"}, 404)
    except Exception as e:
        return make_response("Not a JSON", 400)
