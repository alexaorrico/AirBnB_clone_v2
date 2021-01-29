#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def _places(city_id):
    """retrieves the list of all place objects
    """
    if request.method == "GET":
        all_places = []
        city_info = storage.get(City, city_id)

        if place_info is not None:
            for key in city_info.places:
                all_places.append(key.to_dict())
            return jasonify(city_info)
        abort(404)

    if request.method == 'POST':
        if not request.is_json:
            return "Not a JSON", 400

        city_info = storage.get(City, city_id)
        if city_info is not None:
            kwargs = {"city_id": city_id}
            kwargs.update(request.get_json())
            all_places = Place(**dict)
            dict_info = all_places.to_dict()

        if "user_id" not in dict_info.keys():
            return "Missing user_id", 400

        if not storage.get(User, dict_info.get("user_id")):
            abort(404)

        if "name" not in dict_info.keys():
            return "Missing name", 400

        all_places.save()
        return all_places.to_dict(), 201
    abort(404)


@app_views.route('/places/<places_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places_ident(places_id):
    """updates a place object
    """
    if request.method == "GET":
        place_info = storage.get(Place, places_id)
        if place_info is not None:
            return place_info.to_dict()
        abort(404)

    if request.method == "PUT":
        place_info = storage.get(Place, places_id)
        if place_info is not None:
            if not request.is_json:
                return "Not a JSON", 400

            for key, value in request.get_json().items():
                if key not in ["id",
                               "user_id",
                               "city_id",
                               "created_at",
                               "updated_at"]:
                    setattr(place_info, key, value)
            storage.save()
            return place_info.to_dict(), 200
        abort(404)

    if request.method == "DELETE":
        place_info = storage.get(Place, places_id)
        if place_info is not None:
            place_info.delete()
            storage.save()
            return {}, 200
        abort(404)
