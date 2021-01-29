#!/usr/bin/python3
""" new view for Amenity objects """

from models.amenity import Amenity
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, base_model


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_Amenitys():
    """Retrieves the list of all Amenity objects"""
    if request.method == 'GET':
        Amenity_list = []
        for ob in storage.all(Amenity).values():
            Amenity_list.append(ob.to_dict())
        return jsonify(Amenity_list), 200


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['GET'])
def get_Amenity_id(amenity_id):
    """Retrieves a Amenity by id"""
    if request.method == 'GET':
        ob = storage.get(Amenity, amenity_id)
        if ob is not None:
            return jsonify(ob.to_dict())
        else:
            return jsonify({"error": "Not found"}), 404


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_Amenity_ob(amenity_id):
    """Delete a Amenity object by id"""
    if request.method == 'DELETE':
        ob = storage.get(Amenity, amenity_id)
        if ob is not None:
            storage.delete(ob)
            storage.save()
            return jsonify({}), 200
        else:
            return abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_Amenity_ob():
    """Create a Amenity object"""
    if request.method == 'POST':
        test = request.get_json()
        if not test:
            return "Not a JSON", 400
        elif "name" not in test:
            return "Missing name", 400
        else:
            ob = Amenity(**test)
            storage.new(ob)
            storage.save()
            return jsonify(ob.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['PUT'])
def update_Amenity_ob(amenity_id):
    """Update a Amenity object"""
    if request.method == 'PUT':
        ob = storage.get(Amenity, amenity_id)
        data = request.get_json()
        if not ob:
            return abort(404)
        if not data:
            return "Not a JSON", 400
        for key, val in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(ob, key, val)
        storage.save()
        return jsonify(ob.to_dict()), 200
