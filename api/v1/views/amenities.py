#!/usr/bin/python3
""" View for amenities """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_no_id():
    """ Gets an amenity if no id has been provided """
    amen = storage.all(Amenity).values()
    return jsonify([a.to_dict() for a in amen])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id=None):
    """ Gets an amenity when an id is provided """
    amen = storage.all(Amenity)
    a_key = "Amenity." + amenity_id
    if a_key not in amen:
        abort(404)
    return(jsonify(amen[a_key].to_dict()))


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def new_amenity():
    """ Creates a new amenity """
    js_info = request.get_json()
    if request.is_json is False:
        abort(400, 'Not a JSON')
    if 'name' not in js_info:
        abort(400, 'Missing name')
    new_a = Amenity(**js_info)
    new_a.save()
    return jsonify(new_a.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ Deletes an amenity based on the amenity id """
    amen = storage.all(Amenity)
    a_key = "Amenity." + amenity_id
    if a_key not in amen:
        abort(404)
    storage.delete(amen[a_key])
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """ Updates an amenity based on the amenity id """
    js_info = request.get_json()
    amen = storage.all(Amenity)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_info.pop('id', 'no_error_pls')
    js_info.pop('created_at', 'no_error_pls')
    js_info.pop('updated_at', 'no_error_pls')
    a_key = "Amenity." + amenity_id
    if a_key not in amen:
        abort(404)
    for key, val in js_info.items():
        setattr(amen[a_key], key, val)
    storage.save()
    return jsonify(amen[a_key].to_dict()), 200
