#!/usr/bin/python3
"""script to serve routes related to amenities objects"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
import json
from flask import request, jsonify, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def serve_amenities():
    """Retrieves a list of all amenity objects"""
    amenities = storage.all(Amenity)
    list_amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def serve_amenity_id(amenity_id):
    """Retrives a amenity object"""
    response = storage.get(Amenity, amenity_id)

    if response is None:
        abort(404)

    return jsonify(response.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_obj(amenity_id):
    """deletes a amenity object"""
    amenity_to_delete = storage.get(Amenity, amenity_id)

    if amenity_to_delete is None:
        abort(404)

    storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """creates a amenity"""

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    # if name not in dict
    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    new_amenity = Amenity(name=data_entered.get('name'))
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity_obj(amenity_id):
    """updates a amenity object"""
    amenity_to_update = storage.get(Amenity, amenity_id)

    if amenity_to_update is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    for key, value in data_entered.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_to_update, key, value)

    storage.save()

    return jsonify(amenity_to_update.to_dict()), 200
