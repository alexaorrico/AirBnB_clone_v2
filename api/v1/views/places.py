#!/usr/bin/python3
"""
Create a view for Place objects - handles all default RESTful API actions
"""

# Import necessary modules
from flask import abort, jsonify, request

# Import the required models
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Route for retrieving all Place objects of a City
@app_views.route(
    "/cities/<city_id>/places",
    methods=["GET"],
    strict_slashes=False,
)
def get_places_by_city(city_id):
    """
    Retrieves all Place objects of a specific City
    """
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Get all Place objects of the City from the storage
        places = [place.to_dict() for place in city.places]
        # Return the Place objects in JSON format
        return jsonify(places)
    else:
        # Return 404 error if the City object is not found
        abort(404)


# Route for retrieving a specific Place object by ID
@app_views.route(
    "/places/<place_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_place(place_id):
    """
    Retrieves a Place object by ID
    """
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Return the Place object in JSON format
        return jsonify(place.to_dict())
    else:
        # Return 404 error if the Place object is not found
        abort(404)


# Route for deleting a specific Place object by ID
@app_views.route(
    "/places/<place_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_place(place_id):
    """
    Deletes a Place object by ID
    """
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Delete the Place object from the storage and save changes
        storage.delete(place)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if the Place object is not found
        abort(404)


# Route for creating a new Place object
@app_views.route(
    "/cities/<city_id>/places",
    methods=["POST"],
    strict_slashes=False,
)
def create_place(city_id):
    """
    Creates a new Place object under a specific City
    """
    # Get the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, "Not a JSON")

        # Get the JSON data from the request
        data = request.get_json()
        # Check if the JSON data contains the required attribute
        if "user_id" not in data:
            # Return 400 error if the JSON data does not contain the required attribute
            abort(400, "Missing user_id")
        # Get the User object with the given user_id from the storage
        user = storage.get(User, data["user_id"])
        if not user:
            # Return 404 error if the User object is not found
            abort(404)

        # Check if the JSON data contains the required attribute
        if "name" not in data:
            # Return 400 error if the JSON data does not contain the required attribute
            abort(400, "Missing name")

        # Create a new Place object with the JSON data
        place = Place(**data)
        # Set the city_id attribute of the Place object to the city_id
        place.city_id = city_id
        # Save the new Place object to the storage
        place.save()
        # Return the new Place object in JSON format with 201 status code
        return jsonify(place.to_dict()), 201
    else:
        # Return 404 error if the City object is not found
        abort(404)


# Route for updating an existing Place object by ID
@app_views.route(
    "/places/<place_id>",
    methods=["PUT"],
    strict_slashes=False,
)
def update_place(place_id):
    """
    Updates an existing Place object by ID
    """
    # Get the Place object with the given ID from the storage
    place = storage.get(Place, place_id)
    if place:
        # Check if the request data is in JSON format
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, "Not a JSON")

        # Get the JSON data from the request
        data = request.get_json()
        # Update the Place object with the JSON data
        for key, value in data.items():
            if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
                setattr(place, key, value)
        # Save the updated Place object to the storage
        place.save()
        # Return the updated Place object in JSON format with 200 status code
        return jsonify(place.to_dict()), 200


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    """
    Returns 404: Not Found
    """
    # Return a JSON response for 404 error
    response = {"error": "Not found"}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Return Bad Request message for illegal requests to the API
    """
    # Return a JSON response for 400 error
    response = {"error": "Bad Request"}
    return jsonify(response), 400


# New endpoint: POST /api/v1/places_search
@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending on the JSON in the body of the request
    """
    # Get the JSON data from the request
    data = request.get_json()
    # If the JSON data is empty, return all Place objects
    if not data:
        places = storage.all(Place).values()
        places = [place.to_dict() for place in places]
        return jsonify(places)

    # Get the Place objects that match the JSON data
    places = storage.all(Place).values()
    places = [place.to_dict() for place in places]

    # Filter the Place objects based on the JSON data
    places = [
        place
        for place in places
        if all(key in place and place[key] == value for key, value in data.items())
    ]
    # Return the filtered Place objects in JSON format
    return jsonify(places)
