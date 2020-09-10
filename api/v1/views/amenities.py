#!/usr/bin/python3
"""Create a new view for State objects"""

from flask import jsonify, request, abort
from flask import make_response
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities_list():
    """Retrieves the list of all Amenities objects"""
    if request.method == 'GET':
        all_amenities = []
        for key in storage.all(Amenity).values():
            all_amenities.append(key.to_dict())
        return jsonify(all_amenities)
    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in response:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_amenity = State(**response)
        new_amenity.save()
        return make_response(jsonify(amenities.to_dict()), 201)


@app_views.route("/amenities/<state_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """ Manipulate an specific amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        if amenity:
            return jsonify(amenity.to_dict())
        abort(404)
    if request.method == 'DELETE':
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return make_responce(jsonify({}), 200)
    if request.method == "PUT":
        response = request.get_json()
        if response is None:
            return "Not a JSON", 400
        if amenity is None:
            abort(404)
        for key, value in response.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
             and hasattr(amenity, key):
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
