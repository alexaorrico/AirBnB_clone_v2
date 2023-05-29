#!/usr/bin/python3
""" Blueprint for Amenity objs that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=["GET"], strict_slashes=False)
def amenity(amenity_id=None):
    """ Retrieves Amenity obj """
    if amenity_id is None:
        amenities = storage.all("Amenity")
        my_amenities = [value.to_dict() for key, value in amenities.items()]
        return jsonify(my_amenities)

    my_amenities = storage.get("Amenity", amenity_id)
    if my_amenities is None:
        abort(404)
    else:
        return jsonify(my_amenities.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_amenities(amenity_id):
    """ Deletes a Amenity obj based on its' id """

    my_amenity = storage.get("Amenity", amenity_id)
    if my_amenity is None:
        abort(404)
    storage.delete(my_amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def post_amenities():
    """ Creates a Amenity """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**content)
    new_amenity.save()

    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=["PUT"], strict_slashes=False)
def update_amenities(amenity_id):
    """ Updates a Amenity obj & id """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_amenity = storage.get("Amenity", amenity_id)
    if my_amenity is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_amenity, key, value)

    my_amenity.save()
    return (jsonify(my_amenity.to_dict()), 200)
