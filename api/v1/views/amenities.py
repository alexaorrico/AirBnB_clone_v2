#!/usr/bin/python3
'''
   This module handles all default RestFul API actions for Amenity objects.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities_by_state():
    '''
       Retrieves all Amenity objects from storage
    '''
    amenities = storage.all("Amenity")
    amenities_list = []
    for k, v in amenities.items():
        amenities_list.append(v.to_dict())

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    '''
       Retrieves a specified Amenity object from storage
    '''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    format_amenity = amenity.to_dict()
    return jsonify(format_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''
       Deletes a specified Amenity object from storage
    '''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    '''
       Creates a new Amenity object and saves it to storage
    '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        amenity_dict = request.get_json()
        if "name" in amenity_dict:
            amenity_name = amenity_dict["name"]
            amenity = Amenity(name=amenity_name)
            for k, v in amenity_dict.items():
                setattr(amenity, k, v)
            amenity.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return jsonify({"error": "Missing name"}), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''
       Updates an existing Amenity object and saves it to storage
    '''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    req = request.get_json()
    for k, v in req.items():
        if k != "id" or k != "created_at" or k != "updated_at":
            setattr(amenity, k, v)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
