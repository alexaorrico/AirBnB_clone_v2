#!/usr/bin/python3
"""This is the amenities views"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """This view returns all amenities"""
    return jsonify([amen.to_dict() for amen in storage.all(Amenity).values()])


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """GEt amenity by id"""
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amentiy_by_id(amenity_id):
    """Deletes amenity by id"""
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    storage.delete(amen)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """creates an amenity object"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amen = Amenity(**request.get_json())
    amen.save()
    return jsonify(amen.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """Updates amenity object by id"""
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amen, key, value)
    amen.save()
    return jsonify(amen.to_dict())
