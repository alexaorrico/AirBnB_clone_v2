#!/usr/bin/python3
"""
View for Amenity objects that will handle all default
RESTful API actions
"""
# Allison Edited 11/20 4:45 PM
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amens():
    """retrieves the list of all amenitiy objects"""
    all_amens = storage.all(Amenity).values()
    amen_list = []
    for amenity in all_amens:
        amen_list.append(amenity.to_dict())
    return jsonify(amen_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def one_amenity(amenity_id):
    """retrieves an amenity object when a amenity id is provided
        will return 404 error if amenity is not found."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amen(amenity_id):
    """deletes amenity object specified by amenity_id, returns a 404 error
        if city is not found, returns empty dictionary with status code 200"""
    amen = storage.get(Amenity, amenity_id)
    if not amen:
        abort(404)
    storage.delete(amen)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def new_amenity():
    """Creates a new amenity - transforms the HTTP body request to a dictionary
    handles error raises, returns new state with status code 201"""

    new_data = request.get_json()

    if new_data is None:
        abort(400, description="Not a JSON")
    if 'name' not in new_data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**new_data)
    """** -> double asterisks unpacks a dictionary and passes
    the key-value pairs as arguments to the state constructor!"""
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity based off of amenity id given in request, returns the
    amenity object and status code 200"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    key_ignore = ['id', 'created_at', 'updated_at']

    new_data = request.get_json()
    for key, value in new_data.items():
        if key not in key_ignore:
            setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
