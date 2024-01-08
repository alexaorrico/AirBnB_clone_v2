#!/usr/bin/python3
'''
    RESTFUL API for Amenity class
'''
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''
        return all amenity objects in json form
    '''
    amenities = [amen.to_dict() for amen in storage.all('Amenity').values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_using_id(amenity_id):
    '''
        returns amenity with maching id using http verb GET
    '''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    '''
        delete amenity obj given amenity_id
    '''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''
        create new amenity object
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        obj = Amenity(**data)
        obj.save()
        return jsonify(obj.to_dict(), 201)


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenities_id):
    '''
        update existing amenity object using PUT
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get("Amenity", amenities_id)
    if obj is None:
        abort(404)
    for attr, value in data:
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(obj, attr, value)
    obj.save()
    return (jsonify(obj.to_dict()), 200)
