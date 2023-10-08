#!/usr/bin/python3
"""Endpoints for amenity"""

from flask import request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def getAmenities():
    """Retrieves the list of all Amenity objects"""
    objs = storage.all(Amenity)
    return [obj.to_dict() for obj in objs.values()]


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def getAmenity(amenity_id):
    """Returns Amenity object with id = @amenity_id"""
    amenityObj = storage.get(Amenity, amenity_id)
    if amenityObj is None:
        abort(404)
    return amenityObj.to_dict()


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """Delete Amenity object with id = @amenity_id"""
    amenityObj = storage.get(Amenity, amenity_id)
    if amenityObj is None:
        abort(404)
    amenityObj.delete()
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """Create an Amenity object.
    attrs should be checked in post request.
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing name')
    amenityObj = Amenity()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenityObj, key, value)
    amenityObj.save()
    return amenityObj.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """Updates an Amenity object's attributes"""
    amenityObj = storage.get(Amenity, amenity_id)
    if amenityObj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenityObj, key, value)
    amenityObj.save()
    return make_response(jsonify(amenityObj.to_dict()), 200)
