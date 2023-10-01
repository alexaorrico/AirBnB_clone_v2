#!/usr/bin/python3

from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views, Amenity, stoarge


def to_dict():
    """ retrieve an object into a valid JSON"""
    return jsonify({})

@app_views.route('/api/v1/amenities', method=['GET'])
def amenity_list():
    """ retrieve all list of amenities """
    state = stoarge.get("State", state_id)
    if state is None:
        abort(404)
    all_amenities = [amenities.to_json() for amenities in state.amenities]
    return jsonify(all_amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', method=['GET'])
def amenity_object(amenity_id =None):
    """ retrieve all state object """
    amenity = stoarge.get("Amenity", amenity_id)
    if city is None:
        abort(404)
    return jsonify(amenity.to_json())

@app_views.route('/api/v1/amenities/<amenity_id>', method=['DELETE'])
def amenity_delete(amenity_id =None):
    """ delete all state object """
    if amenity_id is None:
        abort(404)
    amenity = stoarge.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    stoarge.delete(amenity)
    return jsonify({}), 200

@app_views.route('/api/v1/amenities', method=['POST'])
def amenity_create():
    """ create all state object """
    data = None
    try:
        data = request.get_json()
    except:
        data = None
    if data is None:
        return jsonify({"Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"Missing name"}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonifyamenity.to_json()), 201


@app_views.route('/api/v1/amenities/<amenity_id>', method=['PUT'])
def amenity_update(amenity_id = None):
    """ update all state object """
    data = None
    try:
        data = request.get_json()
    except:
        data = None
    if data is None:
        return jsonify({"Not a JSON"}), 400
    amenity = stoarge.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    for keys, values in data.items():
        if keys not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, keys, values)
    amenity.save()
    return jsonify(amenity.to_json()), 200
