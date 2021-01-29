#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>/', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities_get(amenity_id=None):
    """retrieves the list of all State objects
    """
    if request.method == "GET":
        all_amenities = []
        for key in storage.all("Amenity").values():
            all_amenities.append(key.to_dict())
        return jsonify(all_amenities)

    if request.method == 'POST':
        if not request.is_json:
            return "Not a JSON", 400
        all_amenities = Amenity(**request.get_json())
        if "name" not in all_amenities.to_dict().keys():
            return "Missing name", 400
        all_amenities.save()
        return all_amenities.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """deletes a State object
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify(abort(404))
    amenity.delete()
    storage.save()
    dict = {}
    return (jsonify(dict), 200)


@app_views.route('/amenity/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """updates a state object
    """
    info = request.get_json()
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    amenity_info = storage.get("Amenity", state_id)
    if amenity_info is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in info.items():
        if key not in ignore_keys:
            setattr(amenity_info, key, value)

    amenity_info.save()
    return jsonify(amenity_info.to_dict())
