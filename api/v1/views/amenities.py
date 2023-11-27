#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify, abort
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app_views.route('/amenities/', methods=['GET'])
def get_all_amenities():
    """ tbc """
    amenity_list = []
    amenities_dict = storage.all(Amenity)
    for item in amenities_dict:
        amenity_list.append(amenities_dict[item].to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_one_amenities(amenity_id):
    """ tbc """
    amenities_dict = storage.all(Amenity)
    for item in amenities_dict:
        if amenities_dict[item].to_dict()['id'] == amenity_id:
            return jsonify(amenities_dict[item].to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_one_amenities(amenity_id):
    """ tbc """
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is not None:
        storage.delete(the_amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities/', methods=['POST'])
def post_amenity():
    """ tbc """
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    json_dict = request.json
    if 'name' not in json_dict:
        abort(400, description='Missing name')
    new_amenity = Amenity()
    for item in json_dict:
        setattr(new_amenity, item, json_dict[item])
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity_attribute(amenity_id):
    """ tbc """
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    j = request.json
    for i in j:
        if j[i] != 'id' and j[i] != 'created_at' != j[i] != 'updated_at':
            setattr(the_amenity, i, j[i])
    storage.save()
    return jsonify(the_amenity.to_dict()), 200
