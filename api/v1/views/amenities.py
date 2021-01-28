#!/usr/bin/python3
"""
Module that handles the class of State in API
"""
from models.amenity import Amenity
from models import storage
import json
from flask import Flask, jsonify, request, make_respone, abort
from api.v1.views import app_views


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def api_GET_dict(amenity_id=None):
    """Uses  the models class to_dict to retrieve all amenity objects"""
    amenities = storage.all("Amenity")
    all_amenities= []

    if amenity_id is None or amenity_id is "":
        for amenity in amenities.values():
            all_amenities.append(amenity.to_dict())
        return jsonify(all_amenities)
    else:
        for amenity in amenities.values():
            return jsonify(amenity.to_dict())
    abort(404)
    return


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def api_DEL_Amenity(amenity_id):
    """Use models class to delete an instace of class Amenity"""
    amenities = storage.all(Amenity)

    for amenities in amenities.values():
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_view.route('/amenities/<amenity_id>', methods=['POST'],
                strict_slashes=False)
def api_PUT_Amenity(amenity_id):
    """"Method to create an amenity"""
    payload = request.get_josn(silent=True)

    if payload is None:
        abort(400, 'Not a JSON')
    elif 'name' not in payload:
        about(400, 'Missing name')

    new_amenity = (**payload)
    new_amenity.save()

    return(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def api_PUT_Amenity(amenity_id):
    """Method to update a amenity object"""
    payload = request.get_json(silent=True)
    amenities = storage.all(Amenity)

    if payload is None:
        abort(400, 'Not a JSON')

    for amenity in amenities.values():
        if amenity.id == amenity_id:
            for k, v in payload.item():
                if k != 'created_at' and k != 'updated_at' and k != 'id':
                    setattr(amenity, k, v)
            return(jsonify(amenity.to_dict()), 200)
    abort(400)
