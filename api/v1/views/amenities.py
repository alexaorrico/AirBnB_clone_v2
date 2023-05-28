#!/usr/bin/python3
"""
view for Amenity objects that handles all default RESTFul API actions
"""


import json
from models import storage
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieve_amenity():
    """
    Retreves the amenities
    """

    amenities_list = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_amenity_uisng_amenityid(amenity_id):
    """
    Retrieves an amenity using the amenity id
    Raises a 404 error if the id doesnt match any amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    delete an amenity using the amenity_id
    Raises a 404 not found error if the id doesnt exists
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({})
    abort(404)
