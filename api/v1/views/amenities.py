#!/usr/bin/python3
"""
Module Amenity
"""
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """

    """
    # get data
    all_amenities = storage.all(Amenity).values()
    # store each comm
    result = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(result)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_aminity_id(amenity_id):
    """

    """
    # get data
    amenity = storage.get(Amenity, amenity_id)
    # raises 404 error if amenity_id is not linked to an amenity
    if amenity is None:
        abort(404)

    result = amenity.to_dict()
    return jsonify(result)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """

    """
    # get data
    delete_amenity = storage.get(Amenity, amenity_id)
    # raises 404 error if amenity_id is not linked to an amenity
    if delete_amenity is None:
        abort(404)
    else:
        # delete and saves at given amenity_id
        storage.delete(delete_amenity)
        storage.save()
        # returns an empty dict with status 200
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """

    """
    # parses incoming json file
    posted = request.get_json()
    # returns error message and status 400 if not a json file
    if posted is None:
        return jsonify({'error': 'Not a JSON'}), 400
    # returns error message and status 400 if no key 'name'
    if 'name' not in posted:
        return jsonify({'error': 'Mising name'}), 400
    # gets, saves and returns the new amenity with code 201
    new_amenity = Amenity(**posted)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity_id(amenity_id):
    """
    Updates a amenity objects
    """
    # parses incoming json file
    body = request.get_json()
    # returns error and status 400 if not a json file
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    # gets the amenity linked to amenity_id
    amenity = storage.get(State, amenity_id)
    # if amenity_id not linked to a amenity status error 404
    if amenity is None:
        abort(404)
    else:
        # sets ignored keys
        ignore = ['id', 'created_at', 'updated_at']
        # updates the amenity with all key-value pairs of dict
        for key, value in body.items():
            if key not in ignore:
                setattr(amenity, key, value)
            else:
                pass
        # saves and returns object with status 200
        amenity.save()
        return jsonify(amenity.to_dict()), 200
