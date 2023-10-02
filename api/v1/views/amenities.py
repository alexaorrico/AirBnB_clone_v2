#!/usr/bin/python3
"""
    states.py file in v1/views
"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def handle_amenities():
    """
        Method to return a JSON representation of all states
    """
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        all_amenities = []
        for amenity in amenities.values():
            all_amenities.append(amenity.to_dict())
        return jsonify(all_amenities)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        new_amenity = Amenity(**post)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def handle_amenity_by_id(amenity_id):
    """
        Method to return a JSON representation of a state
    """
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(amenity_by_id.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity_by_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity_by_id, key, value)
        storage.save()
        return jsonify(amenity_by_id.to_dict()), 200
