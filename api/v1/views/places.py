#!/usr/bin/python3
"""
places view routes
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    "/cities/<city_id>/places",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def city_places(city_id):
    """Handles /cities/<city_id>/places endpoint

    Returns:
        json: list of all places or the newly added place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "POST":
        try:
            place_data = request.get_json()
            if "user_id" not in place_data:
                return jsonify(error="Missing user_id"), 400
            elif "name" not in place_data:
                return jsonify(error="Missing name"), 400
            else:
                user = storage.get(User, place_data["user_id"])
                if user is None:
                    abort(404)
                place_data["city_id"] = city.id
                place = Place(**place_data)
                storage.new(place)
                storage.save()
                return jsonify(place.to_dict()), 201
        except Exception:
            return jsonify(error="Not a JSON"), 400
    else:
        return jsonify([place.to_dict() for place in city.places])


@app_views.route(
    "/places/<place_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def cities(place_id):
    """Handles /places/<place_id> endpoint

    Returns:
        json: place or empty
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        try:
            place_data = request.get_json()
            for key, value in place_data.items():
                if key not in [
                        "id", "user_id", "city_id", "created_at", "updated_at"
                ]:
                    setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict())
        except Exception:
            return jsonify(error="Not a JSON"), 400
    else:
        return jsonify(place.to_dict())
