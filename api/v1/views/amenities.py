#!/usr/bin/python3
"""amenities register in blueprint instance"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
@app_views.route(
        '/amenities/<amenity_id>',
        methods=['GET'],
        strict_slashes=False)
def amenity_get(amenity_id=None):
    """return all amenities objects"""
    if amenity_id is None:
        amenities = storage.all("Amenity")
        amenities_list = []
        for amenity in amenities.values():
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    else:
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def amenity_delete(amenity_id=None):
    """delete amenity obj"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def amenity_post():
    """add new amenity"""
    response = request.get_json()
    if response is not None:
        if 'name' in response.keys():
            new_amenity = Amenity(**response)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
        else:
            abort(400, description='Missing name')
    else:
        abort(400, description='Not a JSON')


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['PUT'],
        strict_slashes=False)
def amenity_put(amenity_id):
    """update amenity obj"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is not None:
        response = request.get_json()
        if response is not None:
            response.pop("id", None)
            response.pop("created_at", None)
            response.pop("updated_at", None)
            for key, value in response.items():
                setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict()), 200
        else:
            abort(400, description="Not a JSON")
    else:
        abort(404)
