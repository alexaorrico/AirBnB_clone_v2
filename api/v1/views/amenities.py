#!/usr/bin/python3
"""
Router for handling API calls on amenities objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """Get all amenities objects"""
    arrayOfAmenities = []
    for value in storage.all(Amenity).values():
        arrayOfAmenities.append(value.to_dict())
    return jsonify(arrayOfAmenities), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def oneAmenity(amenity_id):
    """Get one amenity based on his id"""
    try:
        amenity = storage.get(Amenity, amenity_id).to_dict()
        return jsonify(amenity), 200
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """Delete one amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """
    Creates a amenity
    """
    if not request.is_json:
        return jsonify(error='Not a JSON'), 400

    body = request.get_json()
    name = body.get('name')
    if not name:
        return jsonify(error='Missing name'), 400

    newAmenity = Amenity(name=name)
    newAmenity.save()
    return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """
    Update a amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        if not request.is_json:
            return jsonify(error='Not a JSON'), 400

        body = request.get_json()
        if 'name' in body:
            amenity.name = body['name']
            amenity.save()
            return jsonify(amenity.to_dict()), 200

        return jsonify(error='Missing name'), 400
