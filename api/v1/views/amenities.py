#!/usr/bin/python3
"""index default view"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def all_amenities():
    """retrieves all Amenity objects by class name"""
    amenities = []
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def amenity(amenity_id):
    """retrieves the number of each objects by amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """retrieves the number of each objects by amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    '''Creates the required test case'''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    amenity = Amenity()
    amenity.name = request.get_json()['name']
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    '''Updates the target amenity with the corressponding id'''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        else:
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
