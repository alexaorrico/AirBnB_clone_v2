#!/usr/bin/python3
""" amenities routes """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """ list of amenities """
    amenities = storage.all('Amenity')
    return jsonify([value.to_dict() for value in amenities.values()])


@app_views.route('/amenities/<string:id>', strict_slashes=False)
def amenity_id(id):
    """ json data of a single amenity """
    single_amenity = storage.get('Amenity', id)
    if single_amenity:
        return jsonify(single_amenity.to_dict()), 200
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def insert_amenity():
    """ Creates a new amenity """
    dictionary = request.get_json()
    if dictionary.get('name') is None:
        abort(400, 'Missing name')
    user = Amenity(**dictionary)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/amenities/<string:id>', strict_slashes=False, methods=['PUT'])
def update_amenity(id):
    """ Updates one amenity """
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a Json')
    single_amenity = storage.get('Amenity', id)
    if single_amenity is None:
        abort(404)
    [setattr(single_amenity, key, value) for key, value in dictionary.items()
        if key not in ['id', 'created_at', 'updated_at']]
    single_amenity.save()
    return jsonify(single_amenity.to_dict())


@app_views.route('/amenities/<string:id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(id):
    """ Deletes one amenity """
    single_amenity = storage.get('Amenity', id)
    if single_amenity is None:
        abort(404, 'Not found')
    single_amenity.delete()
    storage.save()
    return jsonify({})
