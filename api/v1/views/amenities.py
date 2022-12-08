#!/usr/bin/python3
""" Method HTTP for amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Function that retrieves the list of all amenities """
    all_amenities = []
    for amenity in storage.all(Amenity).values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Function that retrieves an Amenity """
    amenity = storage.get(Amenity, amenity_id)
    return abort(404) if amenity is None else jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Function that deletes an Amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Function that create an Amenity """
    dico = request.get_json()

    if dico is None:
        abort(400, "Not a JSON")

    if dico.get("name") is None:
        abort(400, "Missing name")

    new_amenity = Amenity(**dico)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Function that update an Amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)

    dico = request.get_json()

    if dico is None:
        abort(400, "Not a JSON")

    for key, value in dico.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
