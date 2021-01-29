#!/usr/bin/python3
"""new view for Amenity objects that handles all
default RestFul API actions
"""
from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route(
    "/amenities", methods=['GET'], strict_slashes=False)
@app_views.route(
    "/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def amenities_view(amenity_id=None):
    """
    Retrieves the list of all Amenities objects
    """
    if amenity_id:
        am = storage.get(Amenity, amenity_id)
        if am is None:
            abort(404)
        return jsonify(am.to_dict())
    else:
        amenities = [val.to_dict() for val in storage.all(Amenity).values()]
        return jsonify(amenities)


@app_views.route(
    "/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    am = storage.get(Amenity, amenity_id)
    if am is None:
        abort(404)
    storage.delete(am)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an Amenity"""
    content = request.get_json()
    if content:
        if content.get('name'):
            new_amenity = Amenity(**content)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
        abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route(
    "/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    am = storage.get(Amenity, amenity_id)
    if am is None:
        abort(404)
    else:
        content = request.get_json()
        if content:
            keys_ignored = ['id', 'created_at', 'updated_at']
            for key, value in content.items():
                if key not in keys_ignored:
                    setattr(am, key, value)
            am.save()
            return jsonify(am.to_dict()), 200
        else:
            abort(400, "Not a JSON")
