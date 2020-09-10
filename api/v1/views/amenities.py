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
        for key in storage.all("Amenity").values():
            all_amenities.append(key.to_dict())
        return jsonify(all_amenities)
    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if "name" not in response:
            abort(400, "Missing name")
        new_amenity = Amenity(**response)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """ Manipulate an specific amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
                    and hasattr(amenity, key):
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
