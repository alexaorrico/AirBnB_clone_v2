#!/usr/bin/python3
""" amenities view class """
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response


@app_views.route('/amenities', strict_slashes=False, methods=["GET", "POST"])
def get_amenities():
    """ to get all amenities or create new"""
    amenities = storage.all("Amenity")
    if request.method == "GET":
        return jsonify([obj.to_dict() for obj in amenities.values()])
    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("name") is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        amenity = Amenity(**request.get_json())
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_amenity_id(amenity_id=None):
    """ get certian state"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict())
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, val)
        amenity.save()
        return jsonify(amenity.to_dict())
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({})
