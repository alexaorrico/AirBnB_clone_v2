#!/usr/bin/python3
"""
view for Amenity objects that handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def handle_amenities():
    """Retrieves the list of all Amenity objects or
    create a new Amenity object"""
    if request.method == 'GET':
        return jsonify([obj.to_dict() for obj in storage.all("Amenity").
                        values()]), 200
    if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            if not request.get_json(silent=True).get('name'):
                abort(400, "Missing name")
            kwargs = request.get_json(silent=True)
            new_amenity = Amenity(**kwargs)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_byid(amenity_id):
    """Retrieves an Amenity object by id"""
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj:
        if request.method == 'GET':
            return jsonify(amenity_obj.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(amenity_obj)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            kwargs = request.get_json(silent=True)
            if kwargs:
                for key, value in kwargs.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(amenity_obj, key, value)
                amenity_obj.save()
            return jsonify(amenity_obj.to_dict()), 200
    else:
        abort(404)
