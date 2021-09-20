#!/usr/bin/python3
"""
script that starts a Flask web application:
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def amenity_all():
    """
    Retrieves a amenity object:
    """
    list = []
    for amenity in storage.all("Amenity").values():
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def ameny_all(amenity_id):
    """
    Retrieves a amenity object:
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@ app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                  strict_slashes=False)
def amenity_delete(amenity_id):
    """
    Deletes a amenity object
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@ app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """
    Creates a Amenity
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        my_amenity = amenities.Amenity(**request.get_json())
        storage.new(my_amenity)
        storage.save()
        resp = my_amenity.to_dict()
        return jsonify(resp), 201


@ app_views.route('/amenities/<amenity_id>',
                  methods=['PUT'], strict_slashes=False)
def amenity_put(amenity_id):
    """
    Updates a Amenity object
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amt = request.get_json()
    if amt is None:
        abort(400, "Not a JSON")
    else:
        for key, value in amt.items():
            if key in ['id'] and key in ['created_at']\
                    and key in ['updated_at']:
                pass
            else:
                setattr(amenity, key, value)
        storage.save()
        resp = amenity.to_dict()
        return jsonify(resp), 200
