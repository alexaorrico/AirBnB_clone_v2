#!/usr/bin/python3
"""
This is the amenities page endpoints
"""

from api.v1.views import app_views
from flask import jsonify, request
from werkzeug.exceptions import NotFound
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def fetch_amenities(amenity_id=None):
    """Fetches all amenities objects from the database"""
    amenities = storage.all(Amenity)
    if amenity_id:
        for amenity in amenities.values():
            amenity = amenity.to_dict()
            if amenity['id'] == amenity_id:
                return jsonify(amenity)
        raise NotFound
    return jsonify([object.to_dict() for object in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity obj using the amenity id"""
    amenities = storage.all(Amenity)
    if amenity_id:
        for amenity in amenities.values():
            if amenity.id == amenity_id:
                storage.delete(amenity)
                storage.save()
                return jsonify({}), 200
    raise NotFound


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity and saves it to the db"""
    amenity = request.get_json()
    if not amenity:
        return jsonify(error='Not a JSON'), 400
    if 'name' not in amenity:
        return jsonify(error='Missing name'), 400
    amenity = Amenity(**amenity)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """This method updates a amenity's data"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise NotFound
    new_amenity = request.get_json()
    if not new_amenity:
        return jsonify(error='Not a JSON'), 400

    for key, value in new_amenity.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
