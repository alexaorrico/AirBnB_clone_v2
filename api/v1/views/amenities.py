#!/usr/bin/python3
"""Routing for AirBnB amenity object"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False)
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """'GET' response"""
    dic = storage.all(Amenity)
    if amenity_id is None:
        amenities_list = []
        for key, value in dic.items():
            amenities_list.append(value.to_dict())
        return jsonify(amenities_list)
    else:
        for key, value in dic.items():
            if value.id == amenity_id:
                return jsonify(value.to_dict())
        abort(404)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_amenity(amenity_id=None):
    """'DELETE' response"""
    dic = storage.all(Amenity)
    if request.method == 'DELETE':
        empty = {}
        if amenity_id is None:
            abort(404)
        for key, value in dic.items():
            if value.id == amenity_id:
                storage.delete(value)
                storage.save()
                return jsonify(empty), 200
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """'POST' response"""
    dic = storage.all(Amenity)
    flag = 0
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key in body:
        if key == 'name':
            flag = 1
    if flag == 0:
        abort(400, "Missing name")
    new_amenity = Amenity(**body)
    storage.new(new_amenity)
    storage.save()
    new_amenity_dic = new_amenity.to_dict()
    return jsonify(new_amenity_dic), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_amenity(amenity_id=None):
    """'PUT' response"""
    dic = storage.all(Amenity)
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key, value in dic.items():
        if value.id == amenity_id:
            for k, v in body.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)
