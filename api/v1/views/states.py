#!/usr/bin/python3
"""
    Module what creates a new view for City from State
"""
from models import storage
from models.city import City
from models.base_model import BaseModel
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def cities_by_state(state_id):
    '''
        returns cities in state, into json form
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        cities = [c.to_dict() for c in state.cities]
    return jsonify(cities), 200

@app_views.route("cities/<city_id>", methods=['GET'])
def city_obj(city_id):
    """
        method get list the records with city_id
    """
    city = storage.get("City", state_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200

@app_views.route("states/<state_id>", methods=['DELETE'])
def del_state(state_id):
    '''
        return dictionary with state obj
    '''
    state = storage.get("State")
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200

@app_views.route("/states", methods=['POST'])
def create_city(state_id):
    '''
        create new city obj through state association using POST
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        obj_data['state_id'] = state.id
        obj = City(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_city(state_id):
    '''
        update existing city object using PUT
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200