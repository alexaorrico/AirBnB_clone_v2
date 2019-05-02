#!/usr/bin/python3
""" View for Amenity objects """
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort
from models import storage
from models.amenity import Amenity
from models.state import State
from models.city import City

import json


@app_views.route("/amenities", methods=["GET", "POST"],
                  strict_slashes=False)
def amenity_list():
    """ GET: Render a list of amenities 
    """
    if request.method == "POST":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in new_dict:
            return jsonify({"error": "Missing name"}), 400
        new_amenity = Amenity(**new_dict)
        storage.new(new_amenity)
        storage.save()
        storage.close()
        return jsonify(new_amenity.to_dict()), 201
    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()] 
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def detail_amenity(amenity_id):
    """ Work on a specific amenity """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        storage.close()
        return jsonify({})
    if request.method == "PUT":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in new_dict.items():
            if k not in ["id", "updated_at", "created_at"]:
                setattr(amenity, k, v)
        amenity.save()
    return jsonify(amenity.to_dict())
