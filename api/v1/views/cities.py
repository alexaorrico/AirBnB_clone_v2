#!/usr/bin/python3
'''
    RESTful API for class City
'''
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    '''
        return cities in state, json form
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    city_list = [c.to_dict() for c in state.cities]
    return (jsonify(city_list), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    '''
        return city and its id using GET
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''
        DELETE city obj given city_id
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''
        create new city obj through state association using POST
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        data['state_id'] = state.id
        obj = City(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
        update existing city object using PUT
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    for attr, value in data:
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, attr, value)
    obj.save()
    return (jsonify(obj.to_dict()), 200)
