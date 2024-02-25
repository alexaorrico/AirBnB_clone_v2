#!/usr/bin/python3
"""
Creates a view for Amenity objects - handles all default RESTful API actions.
"""

# Import necessary modules
from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Route for retrieving all Amenity objects
@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    # Get all Amenity objects from the storage
    amenities = storage.all(Amenity).values()
    # Convert objects to dictionaries and jsonify the list
    return jsonify([amenity.to_dict() for amenity in amenities])


# Route for retrieving a specific Amenity object by ID
@app_views.route(
    "/amenities/<amenity_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    # Get the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return the Amenity object in JSON format
        return jsonify(amenity.to_dict())
    else:
        # Return 404 error if the Amenity object is not found
        abort(404)


# Route for deleting a specific Amenity object by ID
@app_views.route(
    "/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    # Get the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Delete the Amenity object from the storage
        storage.delete(amenity)
        # Return an empty response with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the Amenity object is not found
        abort(404)


# Route for creating a new Amenity object
@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    # Return 400 error if the request data is not in JSON format
    if not request.get_json():
        abort(400, "Not a JSON")

    # Get the JSON data from the request
    data = request.get_json()
    # Return 400 error if the JSON data does not contain the name key
    if "name" not in data:
        abort(400, "Missing name")

    # Create a new Amenity object with the JSON data
    amenity = Amenity(**data)
    # Save the new Amenity object to the storage
    amenity.save()
    # Return the new Amenity object in JSON format with 201 status code
    return jsonify(amenity.to_dict()), 201


# Route for updating an existing Amenity object by ID
@app_views.route(
    "/amenities/<amenity_id>",
    methods=["PUT"],
    strict_slashes=False,
)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    # Get the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return 400 error if the request data is not in JSON format
        if not request.get_json():
            abort(400, "Not a JSON")

        # Get the JSON data from the request
        data = request.get_json()
        # Update the Amenity object with the JSON data
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        # Save the updated Amenity object to the storage
        amenity.save()
        # Return the updated Amenity object in JSON format with 200 status code
        return jsonify(amenity.to_dict()), 200
    else:
        # Return 404 error if the Amenity object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    """Return Not Found message for non-existent resources."""
    # Return a JSON response for 404 error
    response = {"error": "Not found"}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """Return Bad Request message for invalid resource requests."""
    # Return a JSON response for 400 error
    response = {"error": "Bad request"}
    return jsonify(response), 400
