#!/usr/bin/python3
"""RESTful API for Amenities object """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Retrieves all Amenity objects """
    list_amenities = []
    for amenity in storage.all('Amenity').values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    empty_dict = {}
    amenity.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ Creates a City object """
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, "Not a JSON")
    elif "name" not in my_dict:
        abort(400, "Missing name")
    new_amenity = Amenity(**my_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object"""
    if amenity_id:
        my_dict = request.get_json()
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if my_dict is None:
            abort(400, "Not a JSON")
        for key, value in my_dict.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
