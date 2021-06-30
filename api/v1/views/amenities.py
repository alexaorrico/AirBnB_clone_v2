#!/usr/bin/python3

""" Module to handle amenities RESTful API """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def all_amenities():
    amenities = storage.all(Amenity).values()

    if request.method == 'GET':
        return jsonify(list(map(lambda x: x.to_dict(), amenities)))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        obj = Amenity(**request.get_json())
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE', 'GET', 'PUT'])
def one_amenity(amenity_id):
    amenities = storage.all(Amenity).values()
    amenity = [amenity for amenity in amenities if amenity.id == amenity_id]
    if len(amenity) == 0:
        abort(404)

    if request.method == 'GET':
        return amenity[0].to_dict()

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.get_json().items():
            if k not in ('id', 'created_at', 'updated_at'):
                setattr(amenity[0], k, v)
        storage.save()
        return jsonify(amenity[0].to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(amenity[0])
        storage.save()
        return {}, 200
