#!/usr/bin/python3
"""Define Amenity Routes"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """Define GET /amenities routes with GET and POST methodes.

    GET - Get a list of all Amenity
    POST - Creates a new Amenity
    """
    # GET
    if request.method == "GET":
        return jsonify([amenity.to_dict()
                        for amenity in storage.all("Amenity").values()])

    # POST
    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    if doc.get("name") is None:
        return "Missing name", 400
    amenity = Amenity(**doc)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def amenity_id(amenity_id):
    """Defines /amenities/<amenity_id> with GET, DELETEa and PUT methods

    GET - Get an Amenity object with the given id.
    PUT - Updates an Amenity with the given id
    DELETE - Deletes an Amenity with the given id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    # GET
    if request.method == "GET":
        return jsonify(amenity.to_dict())

    # DELETE
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    # PUT
    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    for k, v in doc.items():
        if k not in ("id", "created_at", "updated_at"):
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
