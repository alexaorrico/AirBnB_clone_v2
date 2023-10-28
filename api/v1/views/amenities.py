#!/usr/bin/python3
'''This module Retrieves the list of all amenity objects,
deletes, updates, creates and gets information of a amenity '''
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities/', strict_slashes=False)
def get_all_amenities():
    ''' retreive all amenities '''
    amenity_objs = storage.all('Amenity')

    return jsonify([obj.to_dict() for obj in amenity_objs.values()])


@app_views.route('/amenities/<amenity_id>/', strict_slashes=False)
def get_an_amenity(amenity_id):
    '''return the amenity with matching id'''
    amenity_objs = storage.all('Amenity')
    key = 'Amenity.{}'.format(amenity_id)

    if key in amenity_objs:
        amenity = amenity_objs.get(key)
        return jsonify(amenity.to_dict())

    abort(404)


@app_views.route('/amenities/<amenity_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    ''' delete amenity matching the id'''
    amenity_objs = storage.all('Amenity')
    key = 'Amenity.{}'.format(amenity_id)

    if key in amenity_objs:
        obj = amenity_objs.get(key)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    ''' create a amenity '''

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if data.get('name') is None:
        abort(400, "Missing name")

    amenity_obj = Amenity(**data)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>/',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    ''' update amenity '''

    data = request.get_json()
    amenity_objs = storage.all('Amenity')
    key = 'Amenity.{}'.format(amenity_id)

    if key not in amenity_objs:
        abort(404)

    if data is None:
        abort(400, "Not a JSON")
    amenity = amenity_objs.get(key)
    for k, v in data.items():
        setattr(amenity, k, v)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
