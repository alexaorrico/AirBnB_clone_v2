#!/usr/bin/python3

"""
create new view for Amenity objects
that handles all default RESTFul API actions
    - retrive a list of Amenity objects
    - retrive an Amenity object by amenity id
    - delete an Amenity object
    - create an Amenity object
    - update an Amenity object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """
    Retrieves the list of all amenity objects
    """
    AmenityList = [amenity.to_dict()
                   for amenity in storage.all(Amenity).values()]
    return jsonify(AmenityList)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Retrieves an Amenity object by the amenity id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object by the amenity id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """
    Creates an amenity
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        new_amenity = Amenity()
        new_amenity.name = request.get_json().get('name')
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    update an Amenity object
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.name = request.get_json().get('name')
    amenity.save()
    return jsonify(amenity.to_dict())
