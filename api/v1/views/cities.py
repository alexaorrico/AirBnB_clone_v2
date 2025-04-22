#!/usr/bin/python3
"""handles all default RESTFul API actions for City"""
from api.v1.views import cities_views
from models import storage
from models.city import City
from models.state import State
from flask import request, jsonify as js


@cities_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_by_state(state_id):
    """retrieves City objects of a State"""
    # retrieve State object tied to state_id
    state = storage.get(State, state_id)
    if isinstance(state, State):
        try:
            return js([city.to_dict() for city in state.cities]), 200
        except Exception as e:
            return js({"error": "{}".format(e)})
    return js({"error": "state Not Found"}), 404


@cities_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """retrieves a City object"""
    city = storage.get(City, city_id)
    # check for a valid City object
    if isinstance(city, City):
        try:
            return js(city.to_dict())
        except Exception as e:
            return js({"error": "{}".format(e)})
    return js({"error": "city Not Found"}), 404


@cities_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes a City object"""
    # check if city exists
    city = storage.get(City, city_id)
    if isinstance(city, City):
        try:
            storage.delete(city)
            storage.save()
            return {}, 200
        except Exception as e:
            return js({"error": "{}".format(e)})
    return js({"error": "city Not Found"}), 404


@cities_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """creates a City object"""
    state = storage.get(State, state_id)
    # check for a valid State returned object
    if not isinstance(state, State):
        return js({"error": "state Not Found"}), 404
    # check for a valid JSON
    if not request.is_json:
            return js({"error": "Not a JSON"}), 400
    # check for a name key in JSON
    try:
        request_info = request.get_json()
        if request_info.get('name'):
            city = City(name=request_info.get('name'), state_id=state_id)
            # and maybe persist new object created
            storage.save()
            return js(city.to_dict()), 201
        return js({"error": "Missing name"})
    except Exception as e:
        js({"error": "{}".format(e)})


@cities_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """updates a City object"""
    city = storage.get(City, city_id)
    # check for a valid City returned object
    if not isinstance(city, City):
        return js({"error": "city Not Found"}), 404
    # check for a valid JSON
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400
    try:
        request_info = request.get_json()
        # keys to remain unchanged
        attrs_to_ignore = ["id", "state_id", "created_at", "updated_at"]
        for attr, value in request_info.items():
            if attr not in attrs_to_ignore:
                city.__setattr__(attr, value)
        # persist changes to storage engine
        storage.save()
        return js(city.to_dict()), 200
    except Exception as e:
        return js({"error": "{}".format(e)})
