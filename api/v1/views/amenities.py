#!/usr/bin/python3
"""Amenity objects that handles all default RestFul API actions"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/", strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities_list = []
    for key, value in storage.all("Amenity").items():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object """
    _status = storage.get('Amenity', amenity_id)
    if _status:
        return jsonify(_status.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete a Amenity object """
    _status = storage.get('Amenity', amenity_id)
    if _status:
        storage.delete(_status)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creatte a Amenity object """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    _data = request.get_json()
    _status = Amenity(**_data)
    storage.new(_status)
    storage.save()
    _response = jsonify(_status.to_dict())
    _response.status_code = 201
    return _response


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Delete a Amenity object """
    if not request.is_json:
        abort(400, "Not a JSON")
    _status = storage.get('Amenity', amenity_id)
    if _status:
        _data = request.get_json()
        if type(_data) is dict:
            to_avoid = ['id', 'created_at', 'updated_at']
            for name, value in _data.items():
                if name not in to_avoid:
                    setattr(_status, name, value)
            storage.save()
            return jsonify(_status.to_dict())
    abort(404)
