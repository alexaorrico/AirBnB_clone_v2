#!/usr/bin/python3
"""
contains endpoints(routes) for amnenity objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route("/amenitie", strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects:
    """
    objs = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(objs)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an  Amenity objects
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenities = [obj.to_dict() for obj in state.cities]
    return jsonify(amenities)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """
    Deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities/", strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """
    Creates an Amenity instance
    """
    valid_json = request.get_json()

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in valid_json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj = Amenity(**valid_json)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    valid_json = request.get_json()

    if not amenity:
        abort(404)

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in valid_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
