#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'])
def amenities_without_id():
    """Create a new amenity or return all the amenities"""
    if request.method == 'GET':
        amenities_list = []
        amenities_dict = storage.all(Amenity)
        for amenity in amenities_dict.values():
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)

    if request.method == 'POST':
        json = request.get_json(silent=True)
        if json is None:
            abort(400, "Not a JSON")
        if json.get('name') is None:
            abort(400, "Missing name")
        amenity = Amenity(**json)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'PUT', 'DELETE'])
def amenities_with_id(amenity_id=None):
    """Perform READ UPDATE DELETE operations on a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity.delete()
        del amenity
        return jsonify({})

    if request.method == 'PUT':
        json = request.get_json(silent=True)
        if json is None:
            abort(400, "Not a JSON")
        amenity.update(**json)
        return jsonify(amenity.to_dict())
