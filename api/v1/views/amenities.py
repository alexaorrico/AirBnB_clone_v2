#!/usr/bin/python3
"""
New view for Amenity objects that handles taht handles all default ResFul API.
"""

from flask import abort
from flask import jsonify
from models.amenity import Amenity
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenties_all(state_id):
    """
    create Amenty objects
    """

    list_amentiy = []

    for amenty in storage.all('Amenity').values():
        list_amenity.append(amenity.to_dict())
    return jsonify(list_amenity)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """
    Return id of the function
    """
    amenityArr = storage.get("Amenity", amenity_id)
    if amenityArr is None:
        abort(404)
    return jsonify(amenityArr.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def get_amenity_delete(amenity_id):
    """
    method Delete onject
    """
    DELArr = storage.get('Amenity', amenity_id)
    if DELArr is None:
        abort(404)
    else:
        storage.delete(DELArr)
        storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def get_amenity_POST():
    """
    State object
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    nw_amenity = Amenity(**request.get_json())
    nw_amenity.save()
    return jsonify(nw_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def set_amenity_PUT(amenity_id):
    """
    method PUT object
    """
    ament = storage.get('Amenity', amenity_id)
    if ament is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(ament, key, value)
    amenity.save()
    return jsonify(ament.to_dict())


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
