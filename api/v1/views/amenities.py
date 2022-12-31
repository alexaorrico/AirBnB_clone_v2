#!/usr/bin/python3
''' amenities.py '''

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_amenities():
    '''Retrieves the list of all Amenity objects'''
    if request.method == "GET":
        amenities = storage.all(Amenity).values()
        amenities = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities)

    if request.method == "POST":
        if not request.is_json:
            abort(400, description="Not a JSON")

        if "name" not in request.json:
            abort(400, description="Missing name")

        amenity_json = request.get_json()
        amenity_obj = Amenity(**amenity_json)
        storage.new(amenity_obj)
        storage.save()

        return jsonify(amenity_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    '''Retrieves a Amenity object'''
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)

    if request.method == "GET":
        return jsonify(amenity_obj.to_dict())

    elif request.method == "DELETE":
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        if not request.is_json:
            abort(400, description="Not a JSON")

        amenity_json = request.get_json()
        not_needed = ["id", "created_at", "updated_at"]
        for attr, attr_value in amenity_json.items():
            if attr not in not_needed:
                setattr(amenity_obj, attr, attr_value)
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict()), 200
