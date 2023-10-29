#!/usr/bin/python3

"""
The Amenity object responsible for managing standard RESTful API operations.

Author: 
Khotso Selading and Londeka Dlamini
"""


from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, make_response, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenities():
    """retrieves of a list of all amenity objects"""
    amenity_object = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenity_object.values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """retrieves specific amenity obj"""
    amenity_object = storage.get(Amenity, amenity_id)

    if not amenity_object:
        abort(404)

    return jsonify(amenity_object.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amenity(amenity_id):
    """deletes specific amenity object"""
    amenity_object = storage.get(Amenity, amenity_id)

    if not amenity_object:
        abort(404)

    amenity_object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """adds new state object to filestorage/database"""
    new_amenity_object = request.get_json()

    if not new_amenity_object:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if new_amenity_object.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)

    amenity = Amenity(**new_amenity_object)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def put_amenity(amenity_id):
    """adds new state object to filestorage/database"""
    amenity_object = storage.get(Amenity, amenity_id)
    new_amenity_object = request.get_json()

    if amenity_object is None:
        abort(404)
    if new_amenity_object is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in new_amenity_object.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(amenity_object, key, value)

    amenity_object.save()
    return make_response(jsonify(amenity_object.to_dict()), 200)
