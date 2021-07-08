#!/usr/bin/python3
"""
module that defines API interactions for Amenity __objects
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """
    defines the amenities route
    Returns: list of all amenity objects
    """
    amenities = storage.all("Amenity").values()

    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["GET"])
def id_for_amenity(amenity_id):
    """
    defines the amenities/<amenity_id> route
    Returns: amenity id or 404 Error if object not linked to Amenity object
    """
    an_amenity = storage.get("Amenity", amenity_id)
    if an_amenity:
        return jsonify(an_amenity.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity_id(amenity_id):
    """
    defines Delete for amenity objects by id
    Returns: if successful 200 and an empty dictionary
             404 if amenity_id is not linked to any Amenity obj
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """
    define how to create a new amenity object
    Returns: 201 on successful creation
             400 "Not a JSON" if HTTP body request is not valid
    """
    try:
        amenities = request.get_json()

        if amenities.get("name") is None:
            return abort(400, 'Missing name')
    except:
        return abort(400, 'Not a JSON')

    new_amenity = Amenity(name=amenities.get("name"))
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def amenity_update(amenity_id):
    """
    defines how an Update to a state is made
    Returns: 200 and the state object if successful
             400 "Not a JSON" if HTTP body request is not valid
             404 if state_id is not linked to any State object
    """
    amenity_data = request.get_json()

    if not amenity_data:
        return abort(400, 'Not a JSON')

    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        return abort(404)

    for key, value in amenity_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()

    return jsonify(amenity.to_dict()), 200
