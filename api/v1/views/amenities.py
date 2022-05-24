#!/usr/bin/python3
""" Amenity """
import json
from models import storage
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """ Retrieves the list of all Amenity objects """
    if request.method == 'GET':
        list_amenities = []
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)

    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if response.get("name") is None:
            abort(400, "Missing name")

        new = Amenity(**response)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """ Do some methods on an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ignore = ["id", "created_at", "updated_at"]
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key not in ignore:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
