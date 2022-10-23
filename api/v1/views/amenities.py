#!/usr/bin/python3
""" Amenities view """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Returns a list of all the amenities """
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity(amenity_id):
    """ Returns an amenity by id """
    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity from storage based on id """
    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """ Creates a new amenity """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    amenity = Amenity()
    amenity.name = request.get_json()['name']
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an amenity specified by id """
    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, value in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(amenity, key, value)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
