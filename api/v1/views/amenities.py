#!/usr/bin/python3
"""
module: amenity  api
"""
from api.v1.views import app_views, storage, Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ returns all amenities """
    amenity_objs = storage.all('Amenity').values()
    amenities = [amenity.to_json() for amenity in amenity_objs]

    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities_byID(amenity_id=None):
    """ returns amenity by id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return(jsonify(amenity.to_json()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities_byID(amenity_id=None):
    """ delete amenity by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:  # <--- changed from 'if not amenity'
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200  # <--- 200 code was missing


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ creates an amenity  """
    try:
        response = request.get_json()
    except:
        response = None

    if response is None:
        return 'Not a JSON', 400

    if 'name' not in response.keys():
        return 'Missing name', 400
    amenity = Amenity(**response)
    amenity.save()
    return jsonify(amenity.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities_byID(amenity_id=None):
    """ update an amenityby id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    try:
        response = request.get_json()
    except:
        response = None
    if response is None:
        return "Not a JSON", 400
    for item in ("id", "created_at", "updated_at"):
        response.pop(item, None)
    for k, v in response.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_json()), 200
