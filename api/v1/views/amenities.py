#!/usr/bin/python3
"""HolbertonBnB Amenity view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
@swag_from("../apidocs/amenities/get_amenities.yml", methods=["GET"])
@swag_from("../apidocs/amenities/post.yml", methods=["POST"])
def amenities():
    """Defines GET and POST methods for the /amenities route.

    GET - Retrieves a list of all Amenity objects.
    POST - Creates a Amenity.
    """
    # GET method
    if request.method == "GET":
        return jsonify([a.to_dict() for a in storage.all("Amenity").values()])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
@swag_from("../apidocs/amenities/get_amenity_id.yml", methods=["GET"])
@swag_from("../apidocs/amenities/delete.yml", methods=["DELETE"])
@swag_from("../apidocs/amenities/put.yml", methods=["PUT"])
def amenity_id(amenity_id):
    """Defines GET, PUT and DELETE methods for a specific ID on /amenities.

    GET - Retrieves an Amenity object with the given id.
    PUT - Updates an Amenity object with the given id using JSON key/values.
    DELETE - Deletes an Amenity object with the given id.
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify(amenity.to_dict())

    # DELETE method
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "created_at", "updated_at"}
    [setattr(amenity, k, v) for k, v in data.items() if k not in avoid]
    amenity.save()
    return jsonify(amenity.to_dict())
