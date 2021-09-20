#!/usr/bin/python3
""" View Amenity """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"])
def amenityAll():
    """Retrieves all amenities with a list of objects"""
    amenities_list = []
    all_amenities = storage.all(Amenity).values()
    for amenity in all_amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)



@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def amenityId(id):
    """id Amenity retrieve json object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def amenityDel(id):
    """delete Amenity with id"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/amenities/', methods=['POST'])
def amenityPost():
    """ POST a new amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenityPut(id):
    """ Update a amenity object """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
