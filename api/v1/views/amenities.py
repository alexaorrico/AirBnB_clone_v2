#!/usr/bin/python3
"""
module amenities.py
"""

from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenityObjects():
    """ Retrieves the list of all Amenity objects """
    amenity = storage.all(Amenity)
    amenityList = []
    for amen in amenity.values():
        amenityDict = amen.to_dict()
        amenityList.append(amenityDict)
    """states_list = [state.to_dict() for state in states.values()]"""
    return jsonify(amenityList)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def ametityObjectWithId(amenity_id):
    """Retrieves an Amenity object with it's id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenityDeleteWithId(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """Creates an Amenity: POST /api/v1/amenities"""

    """same as 'if not request.is_json'"""
    if request.headers.get('Content-Type') != "application/json":
        abort(400, description="Not a JSON")

    newAmenData = request.get_json()

    if not newAmenData.get("name"):
        abort(400, description="Missing name")

    newAmenObj = Amenity(**newAmenData)
    storage.new(newAmenObj)
    storage.save()

    return jsonify(newAmenObj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """Updates an Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    amenUpdateData = request.get_json()
    amenityObj = storage.get(Amenity, amenity_id)
    if amenityObj:
        ignoredKeys = ['id', 'created_at', 'updated_at']
        for k, v in amenUpdateData.items():
            if k not in ignoredKeys:
                setattr(amenityObj, k, v)
        storage.save()
        return jsonify(amenityObj.to_dict()), 200
    else:
        abort(404)
