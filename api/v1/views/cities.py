#!/usr/bin/python3
"""Routing for AirBnB city object"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_city(state_id=None):
    """'GET' response"""
    dic = storage.all(City)
    if state_id is None:
        abort(404)
    else:
        for key, value in dic.items():
            if value.state_id == state_id:
                return jsonify(value.to_dict())
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id=None):
    """'GET' response"""
    dic = storage.all(City)
    if city_id is None:
        abort(404)
    else:
        for key, value in dic.items():
            if value.id == city_id:
                return jsonify(value.to_dict())
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """'DELETE' response"""
    dic = storage.all(City)
    if request.method == 'DELETE':
        empty = {}
        if city_id is None:
            abort(404)
        for key, value in dic.items():
            if value.id == city_id:
                storage.delete(value)
                storage.save()
                return jsonify(empty), 200
        abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def post_city(state_id=None):
    """'POST' response"""
    dic = storage.all(State)
    flag = 0
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key, value in body.items():
        if key == 'name':
            flag += 1
    for key, value in dic.items():
        if value.id == state_id:
            flag += 1
    if flag != 2:
        abort(400, "Missing name")
    body['state_id'] = state_id
    new_city = City(**body)
    storage.new(new_city)
    storage.save()
    new_city_dic = new_city.to_dict()
    return jsonify(new_city_dic), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """'PUT' response"""
    dic = storage.all(City)
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key, value in dic.items():
        if value.id == city_id:
            for k, v in body.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)
