#!/usr/bin/python3
"""
Module that handles the class of State in API
"""
from models.amenity import Amenity
from models import storage
import json
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/amenities/', strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amen(amenity_id=None):
    """Uses  the models class to_dict to retrieve all amenity objects"""
    amenities = storage.all(Amenity)
    all_amenities = []

    if amenity_id is None or amenity_id is "":
        for amenity in amenities.values():
            all_amenities.append(amenity.to_dict())
        return jsonify(all_amenities)
    else:
        for amenity in amenities.values():
            if amenity.id == amenity_id:
                return jsonify(amenity.to_dict())
    abort(404)
    return


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amen(amenity_id):
    """Use models class to delete an instace of class Amenity"""
    amenities = storage.all(Amenity)

    for amenity in amenities.values():
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def post_amen():
    """"Method to create an amenity"""
    payload = request.get_json(silent=True)

    if payload is None:
        abort(400, 'Not a JSON')
    elif 'name' not in payload:
        abort(400, 'Missing name')

    new_amenity = Amenity(**payload)
    new_amenity.save()

    return(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amen(amenity_id):
    """Method to update a amenity object"""
    payload_amen = request.get_json(silent=True)
    amenities = storage.all(Amenity)

    if payload_amen is None:
        abort(400, 'Not a JSON')

    for amenity in amenities.values():
        if amenity.id == amenity_id:
            for k, v in payload_amen.items():
                if k != 'created_at' and k != 'updated_at' and k != 'id':
                    setattr(amenity, k, v)
            amenity.save()
            return(jsonify(amenity.to_dict()), 200)
    abort(400)
