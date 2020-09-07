#!/usr/bin/python3
""" This module starts the flask application for amenities"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """ GET method to list every amenity """
    amenities_list = []
    for amenity in storage.all('Amenity').values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """ POST method to post a new Amenity """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False)
def get_amenities_id(amenity_id):
    """ GET method to get an amenity by some ID """
    for amenity in storage.all('Amenity').values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def del_amenities_id(amenity_id):
    """ DELETE method to delete amenity object by ID """
    catch_amenity = storage.get('Amenity', amenity_id)
    if catch_amenity is None:
        abort(404)
    storage.delete(catch_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_amenities_id(amenity_id):
    """ PUT method to update values in amenity by ID """
    catch_amenity = storage.get('Amenity', amenity_id)
    if catch_amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(catch_amenity, key, value)
    storage.save()
    return jsonify(catch_amenity.to_dict()), 200
