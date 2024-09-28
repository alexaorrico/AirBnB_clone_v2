#!/usr/bin/python3
"""
    This Module contains all the Amenities Routes
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, jsonify, request


@app_views.route('/amenities', strict_slashes=True, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=True,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """
        This Method returns all the Amenities

        Arguments:
            amenity_id: the amenity Id to be returned or None.

        Return:
            this method returns the amenity value to be returned or All
            if the amenit_id is None.
    """
    amenities = []
    if amenity_id is None:
        for amenity in storage.all(Amenity).values():
            amenities.append(amenity.to_dict())
        return jsonify(amenities), 200
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=True,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """
        This Method deletes the amenity instance
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', strict_slashes=True, methods=['POST'])
def post_amenity():
    """
        This method creates an instances of amenities
    """
    if request.content_type != 'application/json':
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "name" not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=True,
                 methods=['PUT'])
def put_amenity(amenity_id):
    """
        This method creates Updates the Attributes of an instance of a class

        Argument:
            amenity_id: This is the amenity id
        Return: a jsonify object of the updated instance with a status code of
            200 when succesful
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.content_type != "application/json":
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
