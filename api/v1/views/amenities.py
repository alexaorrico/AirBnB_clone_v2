#!/usr/bin/python3
""" Create a new view for amenity objects that handles all
    default RESTFul API actions
"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_No(amenity_id=None):
    """ Retrieves the list of all Amenity objects """
    lista = []
    if amenity_id is None:
        for value in storage.all("Amenity").values():
            lista.append(value.to_dict())
        return jsonify(lista), 200
    else:
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def amenity_del(amenity_id=None):
    """ delete a object if it is into amenitys"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenities():
    """post method amenitys, You must use request.get_json from Flask"""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in json_data.keys():
        return jsonify({'error': "Missing name"}), 400
    amenity = Amenity(**json_data)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id=None):
    """ method put Updates a Amenity object: PUT """
    p_amenity = storage.get("Amenity", amenity_id)
    if p_amenity is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_amenity, key, value)
    storage.save()
    return jsonify(p_amenity.to_dict()), 200
