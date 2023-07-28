#!/usr/bin/python3
"""Create the amenities function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
import models


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """retrieves all amenities"""
    all_state = []
    for enu in models.storage.all("Amenity").values():
        all_state.append(enu.to_dict())
    return jsonify(all_state)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_a_amenity_with_id(amenity_id):
    """get an amenity using id"""
    answer = models.storage.get("Amenity", amenity_id)
    if answer:
        return jsonify(answer.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_a_ameniity_with_id(amenity_id):
    """delete an amenity using id"""
    answer = models.storage.get("Amenity", amenity_id)
    if answer:
        answer.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def add_a_amenity():
    """create n amenity"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    values = request.get_json()
    new_state = Amenity(**values)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_a_amenity_with_id(amenity_id):
    """get a amenity using id"""
    answer = models.storage.get("Amenity", amenity_id)
    if answer:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in request.get_json().items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(answer, k, v)
        answer.save()
        return jsonify(answer.to_dict()), 200
    abort(404)
