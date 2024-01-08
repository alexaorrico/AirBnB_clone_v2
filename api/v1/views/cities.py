#!/usr/bin/python3
"""
handles REST API actions for State
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    '/states/<string:state_id>/cities',
    methods=['GET', 'POST'],
    strict_slashes=False)
def states_cities(state_id):
    """handles states route"""
    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(
            [obj.to_dict() for obj in my_state.cities])
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None or type(post_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        new_name = post_data.get('name')
        if new_name is None:
            return jsonify({'error': 'Missing name'}), 400
        new_state = City(state_id=state_id, **post_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route(
    '/cities/<string:city_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False)
def city_with_id(city_id):
    """handles states route with a parameter state_id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        put_data = request.get_json()
        if put_data is None or type(put_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        to_ignore = ['id', 'created_at', 'updated_at', 'state_id']
        city.update(to_ignore, **put_data)
        return jsonify(city.to_dict()), 200
