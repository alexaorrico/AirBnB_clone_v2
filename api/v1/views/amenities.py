#!/usr/bin/python3
"""This handles views for amenities"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import request, abort
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """This returns all amenities"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return json.dumps(amenities_list, indent=2)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_id(amenity_id):
    """Returns the amenity with that id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return json.dumps(amenity.to_dict(), indent=2)


@app_views.route(
        'amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_amenity(amenity_id):
    """This deletes a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return json.dumps({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """This function creates an amenity"""
    amenity_to_create = request.get_json()
    if not amenity_to_create:
        abort(400, "Not a JSON")
    if "name" not in amenity_to_create:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_to_create)
    new_amenity.save()
    return json.dumps(new_amenity.to_dict(), indent=2), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update the Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data_to_put = request.get_json()
    if not data_to_put:
        abort(400, "Not a JSON")
    for key, value in data_to_put.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return json.dumps(amenity.to_dict(), indent=2), 200
