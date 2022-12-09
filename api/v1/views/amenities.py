#!/usr/bin/python3
"""
index
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['GET'])
def get_amenities():
    """ Get All amenities"""
    amenities = storage.all(Amenity).values()

    return jsonify([amenities.to_dict() for amenities in amenities])


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """ Get State with Id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ DELETE amenity With id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['POST'])
def post_amenity():
    """ Crate amenity"""
    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = Amenity(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity(amenity_id):
    """UPDATE a single amenity"""
    found = storage.get(Amenity, amenity_id)
    if not found:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in invalid:
                    setattr(found, key, value)
            storage.save()
            return jsonify(found.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
