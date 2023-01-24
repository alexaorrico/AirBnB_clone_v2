#!/usr/bin/python3
"""Creating amenity objects to handle all default RESTFUL APIs"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from models.base_model import BaseModel


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieving all amenities from the database"""
    amenity_list = []
    amenities = storage.all(Amenity).values()

    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
        return (jsonify(amenity_list))


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creating new amenity to the list"""
    data = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    amenity.save()
    amenity.save()
    return (jsonify(amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Updating invidual amenities by their ids"""
    one_amenity = storage.get(Amenity, amenity_id)
    
    if not amenity:
        abort(404)

    if request.method == "GET":
        result = one_amenity.to_dict()
        return (jsonify(one_amenity))

    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(amenity, key, value)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deleting an amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
