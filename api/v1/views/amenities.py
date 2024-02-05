#!/usr/bin/python3
"""RESTful API view to handle actions for 'Amenity' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def amenities_routes():
    """
    GET: Retrieves the list of all Amenity objects
    POST: Creates an Amenity object
    """
    if request.method == "GET":
        amenities = [amenity.to_dict() for amenity
                     in storage.all(Amenity).values()]
        return jsonify(amenities)

    if request.method == "POST":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        name = in_data.get("name")
        if name is None:
            return "Missing name\n", 400

        amenity = Amenity(**in_data)
        amenity.save()
        return amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def amenity_id_routes(amenity_id):
    """
    GET: Retrieves the Amenity where id == amenity_id
    PUT: Updates the Amenity that has id == amenity_id
    DELETE: Deletes the Amenity that has id == amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == "GET":
        return jsonify(amenity.to_dict())

    elif request.method == "PUT":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        for key, val in in_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, val)
        amenity.save()
        return amenity.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
