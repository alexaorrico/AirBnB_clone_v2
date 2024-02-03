#!/usr/bin/python3
"""This module contains the view for the amenity resource."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False,)
def amenitys(amenity_id=None):
    if request.method == 'GET':
        if amenity_id is None:
            return jsonify(
                [amenity.to_dict()
                    for amenity in storage.all(Amenity).values()]
            )
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        body = request.get_json(force=True)
        if body.get('name', None) is None:
            return jsonify({'error': 'Missing name'}), 400
        new_amenity = Amenity(**body)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    elif request.method == 'PUT':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404)
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        body = request.get_json(force=True)
        for name, value in {
            k: v
            for k, v in body.items()
            if k not in ['id', 'created_at', 'updated_at']
        }.items():
            setattr(amenity, name, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    elif request.method == 'DELETE':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404, jsonify({}))
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    abort(405)
