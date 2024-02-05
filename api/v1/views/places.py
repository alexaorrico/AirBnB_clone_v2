#!/usr/bin/python3
"""RESTful API view to handle actions for 'Place' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def city_places_routes(city_id):
    """
    GET: Retrieves the list of all Place objects in the city where
         id == city_id
    POST: Creates a Place object in the city where id == city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    elif request.method == "POST":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        user_id = in_data.get("user_id")
        if user_id is None:
            return "Missing user_id\n", 400

        user = storage.get(User, user_id)
        if user is None:
            abort(404)

        name = in_data.get("name")
        if name is None:
            return "Missing name\n", 400

        in_data["city_id"] = city_id
        place = Place(**in_data)
        place.save()
        return place.to_dict(), 201


@app_views.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def place_id_routes(place_id):
    """
    GET: Retrieves the Place where id == place_id
    PUT: Updates the Place that has id == place_id
    PUT: Deletes the Place that has id == place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        return jsonify(place.to_dict())

    elif request.method == "PUT":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        for key, val in in_data.items():
            if key not in ["id", "user_id", "city_id", "created_at",
                           "updated_at"]:
                setattr(place, key, val)
        place.save()
        return place.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
