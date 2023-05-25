#!/usr/bin/python3
""" Configures RESTful api for the places route """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route("cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def places(city_id):
    """ configures the places route """

    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        places_dict = [place.to_dict() for place in city.places]

        return jsonify(places_dict)
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        try:
            user_id = json_dict["user_id"]
        except KeyError:
            abort(400, "Missing user_id")

        user = storage.get("User", user_id)
        if not user:
            abort(404)

        try:
            name = json_dict["name"]
        except KeyError:
            abort(400, "Missing name")

        new_place = Place()
        new_place.user_id = user_id
        new_place.city_id = city_id
        new_place.name = name
        new_place.number_rooms = json_dict.get("number_rooms")
        new_place.number_bathrooms = json_dict.get("number_bathrooms")
        new_place.description = json_dict.get("description")
        new_place.max_guest = json_dict.get("max_guest")
        new_place.price_by_night = json_dict.get("price_by_night")
        new_place.latitude = json_dict.get("latitude")
        new_place.longitude = json_dict.get("longitude")

        storage.new(new_place)
        storage.save()

        return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def places_id(place_id):
    """ configures the places/<place_id> route """

    place = storage.get("Place", place_id)

    if not place:
        abort(404)

    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()

        return jsonify({}), 200
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        keys_to_ignore = [
                "id", "user_id", "city_id",
                "created_at", "updated_at"
        ]
        for key, val in json_dict.items():
            if key not in keys_to_ignore:
                setattr(place, key, val)

        storage.new(place)
        storage.save()

        return jsonify(place.to_dict()), 200
