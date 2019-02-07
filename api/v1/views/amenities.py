#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import OperationalError


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """ Returns all the amenities in json """
    amenities = storage.all('Amenity').values()
    return jsonify([amen.to_dict() for amen in amenities])


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """ makes a new amenity """
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        amenity_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in amenity_json:
        return jsonify(error="Missing name"), 400
    amenity = Amenity(**amenity_json)
    try:
        amenity.save()
    except OperationalError:
        return jsonify(error="Missing name"), 400
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_one_amenity(amenity_id):
    """ Returns specified amenity obj in json """
    if amenity_id:
        amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """ deletes the specified amenity """
    if amenity_id:
        amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """ updates an amenity """
    if amenity_id:
        amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        amenity_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400
    """ remove the unwanted params """
    if amenity_json.get('id'):
        amenity_json.pop('id')
    if amenity_json.get('created_at'):
        amenity_json.pop('created_at')
    if amenity_json.get('updated_at'):
        amenity_json.pop('updated_at')
    for k, v in amenity_json.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
