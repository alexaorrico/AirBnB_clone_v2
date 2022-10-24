#!/usr/bin/python3
"""Routings for amenity-related API requests"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_methods():
    """ get all instance of amenity """
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        return jsonify([i.to_dict() for i in amenities.values()])


@app_views.route('/amenities/<string:id>', methods=['GET'],
                 strict_slashes=False)
def get_single_amenity(id):
    """"get an instance of amenity """
    if request.method == 'GET':
        amenity = storage.get(Amenity, id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(id):
    """ delete an instance of amenity """
    if requestt.method == 'DELETE':
        amenity = storage.get(Amenity, id)
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def add_amenity():
    """ create an instance of amenity """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    body = request.get_json()
    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**body)
    new_amenity.save()
    if storage.get(Amenity, new_amenity.id) is not None:
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(id):
    """ update an instance of amenity """
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    body = request.get_json()
    keys_except = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in keys_except:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
