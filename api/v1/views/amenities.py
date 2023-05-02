#!/usr/bin/python3
"""

"""


from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ """
    amenities = storage.all(Amenity).values()

    amenities_list = [amenity.to_dict() for amenity in amenities]

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """"""
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')

    if 'name' not in data:
        abort(400, description='Missing name')

    amenity = Amenity(**data)
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 200)
