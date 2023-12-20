#!/usr/bin/python3
""" amenities function """


from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', method=['GET'], strict_slashes=False)
def get_amenities():
    """ get amenities object """
    amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>',
                 method=['GET]'], strict_slashes=False)
def get_amenity(amenity_id):
    """ amenity object """

    amenity = storage.get(Amenity, amenity_id)

    if Amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 method=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity if not exist """

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(Amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 method=['POST'], strict_slashes=False)
def post_amenity():
    """ create an amenity """

    json_request = request.get_json()

    if json_request is None:
        abort(404), ("Not a JSON")

    if 'name' not in json_request:
        abort(404), ("Missing name")

    amenity = Amenity(**json_request)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 method=['PUT'], strict_slashes=False)
def update_amenety(amenity_id):
    """ update amenity object """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    json_request = request.get_json()

    if json_request is None:
        abort(400, "Not a JSON")

    for key, value in json_request.item():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
