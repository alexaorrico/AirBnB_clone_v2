#!/usr/bin/python3
''' amenities viewer '''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAmenities():
    ''' get amenity information for all amenities '''
    amenitiesList = []
    for amenity in storage.all("Amenity").values():
        amenitiesList.append(amenity.to_dict())
    return jsonify(amenitiesList)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenity(amenity_id):
    ''' get amenity information for specified amenity '''
    amenitySelect = storage.get("Amenity", amenity_id)
    if amenitySelect is None:
        abort(404)
    return jsonify(amenitySelect.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    ''' deletes an amenity based on its amenity_id '''
    amenityDelete = storage.get("Amenity", amenity_id)
    if amenityDelete is None:
        abort(404)
    amenityDelete.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def postAmenity():
    ''' create a new amenity '''
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenityPost = Amenity(**request.get_json())
    amenityPost.save()
    return make_response(jsonify(amenityPost.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def putAmenity(amenity_id):
    """update an amenity"""
    amenityUpdate = storage.get("Amenity", amenity_id)
    if amenityUpdate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, value in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenityUpdate, attr, value)
    amenityUpdate.save()
    return jsonify(amenityUpdate.to_dict())
