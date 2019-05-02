#!/usr/bin/python3
"""Routing for AirBnB place object"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """'GET' response"""
    dic = storage.all(Place)
    if request.method == 'GET':
        if place_id is None:
            places_list = []
            for key, value in dic.items():
                places_list.append(value.to_dict())
            return jsonify(places_list)
        else:
            for key, value in dic.items():
                if value.id == place_id:
                    return jsonify(value.to_dict())
            abort(404)


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_place(place_id=None):
    """'DELETE' response"""
    dic = storage.all(Place)
    if request.method == 'DELETE':
        empty = {}
        if place_id is None:
            abort(404)
        for key, value in dic.items():
            if value.id == place_id:
                storage.delete(value)
                storage.save()
                return jsonify(empty), 200
        abort(404)


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def post_place():
    """'POST' response"""
    dic = storage.all(Place)
    flag = 0
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key in body:
        if key == 'name':
            flag = 1
    if flag == 0:
        abort(400, "Missing name")
    new_place = Place(**body)
    storage.new(new_place)
    storage.save()
    new_place_dic = new_place.to_dict()
    return jsonify(new_place_dic), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """'PUT' response"""
    dic = storage.all(Place)
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key, value in dic.items():
        if value.id == place_id:
            for k, v in body.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)
