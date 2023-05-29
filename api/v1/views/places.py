#!/usr/bin/python3
""" Blueprint for Place objs that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/places', methods=["GET"], strict_slashes=False)
@app_views.route('/places/<place_id>',
                 methods=["GET"], strict_slashes=False)
def place(place_id=None):
    """ Retrieves Place obj """
    if place_id is None:
        places = storage.all("Place")
        my_places = [value.to_dict() for key, value in places.items()]
        return (jsonify(my_places), 200)

    my_places = storage.get("Place", place_id)
    if my_places is None:
        abort(404)
    else:
        return (jsonify(my_places.to_dict()), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def place_by_city(city_id):
    city_object = storage.get("City", city_id)
    if not city_object:
        abort(404)
    my_places_list = [my_places.to_dict() for my_places in city_object.places]
    return (jsonify(my_places_list), 200)


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_places(place_id):
    """ Deletes a Place obj based on its' id """

    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)
    storage.delete(my_place)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def post_places(city_id):
    """ Creates a Place """
    content = request.get_json()
    if not content:
        return (jsonify({"error": "Not a JSON"}), 400)
    city_object = storage.get("City", city_id)
    if city_object is None:
        abort(404)

    if "user_id" not in content:
        return (jsonify({"error": "Missing user_id"}), 400)
    if "name" not in content:
        return (jsonify({"error": "Missing name"}), 400)

    new_place = Place(**content)
    new_place.city_id = city_id
    storage.new(new_place)
    new_place.save()

    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=["PUT"], strict_slashes=False)
def update_places(place_id):
    """ Updates a Place obj & id """
    content = request.get_json()
    if not content:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)

    not_allowed = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_place, key, value)

    my_place.save()
    return (jsonify(my_place.to_dict()), 200)
