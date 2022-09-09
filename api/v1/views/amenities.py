#!/usr/bin/python3
"""
Amenity
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """
    Retrieves the list of all Amenity objects
    """
    amenities = storage.all("Amenity")
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return(jsonify(amenities_list))


@app_views.route('amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """
    Retrieves a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a Amenity
    """
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    if "name" not in request.get_json():
        no_name = {"error": "Missing name"}
        return (jsonify(no_name), 400)
    obj_dict = request.get_json()
    amenity = Amenity(**obj_dict)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    obj_dict = request.get_json()
    amenity.name = obj_dict["name"]
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
