#!/usr/bin/python3
"""
    This module creates a new view for Place
    objects that handles all default REST API
    actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'], strict_slashes=False)
def get_places_in_city(city_id):
    """Get places in a given city"""
    city = storage.get(City, city_id)
    if city:
        places = city.places
        place_list = []
        for place in places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get a specific place from the db"""
    search_result = storage.get(Place, place_id)
    if search_result:
        return jsonify(search_result.to_dict())
    abort(404)


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a specific place from the db"""
    search_result = storage.get(Place, place_id)
    if search_result:
        storage.delete(search_result)
        storage.save()
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_new_place(city_id):
    """Post a new place to the db"""
    city = storage.get(City, city_id)
    if city:
        try:
            place_dict = request.get_json()
            place_dict.update({"city_id": city_id})

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        u_id = place_dict.get("user_id")
        if u_id:
            usr = storage.get(User, u_id)
            if usr:

                if place_dict.get("name"):
                    new_place = Place(**place_dict)
                    storage.new(new_place)
                    storage.save()
                    return jsonify(new_place.to_dict()), 201

                else:
                    return jsonify({"error": "Missing name"}), 400
            else:
                abort(404)
        return jsonify({"error": "Missing user_id"}), 400

    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def modify_place(place_id):
    """Modify an existing place in the db"""
    place = storage.get(Place, place_id)
    if place:
        try:
            update_dict = request.get_json()
            for key in ('id', 'created_at', 'updated_at'):
                if update_dict.get(key):
                    del update_dict[key]

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in update_dict.items():
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200

    else:
        abort(404)
