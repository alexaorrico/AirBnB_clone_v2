#!/usr/bin/python3
"""Handles the amenities view
"""

# from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Gets the dict containing all the states
    """
    amenities = storage.all("Amenity")
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Gets a amenity by its ID
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an amenity
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in got_json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amen = Amenity(**got_json)
    storage.new(new_amen)
    storage.save()
    return make_response(jsonify(new_amen.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an amenity
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        for key, val in got_json.items():
            setattr(amenity, key, val)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        abort(404)
