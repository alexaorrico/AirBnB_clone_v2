#!/usr/bin/python3
"""Create a new view for Place"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State
from models import City
from models import Amenity
from models import User
from models import Place


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def city_places(city_id):
    '''Retrives a list of all the places in a city'''

    my_city = storage.get("City", city_id)
    if my_city is None:
        abort(404)

    my_places = my_city.places
    my_places = [place.to_dict() for place in my_places]

    return (jsonify(my_places), 200)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_retriever(place_id):
    ''' Retrieves places based on their id'''

    my_places = storage.get("Place", place_id)
    if my_places is None:
        abort(404)
    return (jsonify(my_places.to_dict()), 200)


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    '''deletes a place based on its id'''

    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)
    my_place.delete()

    return (jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    ''' creates a place linked to a city using the city id'''

    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_city = storage.get("City", city_id)
    if my_city is None:
        abort(404)

    user_id = content.get("user_id")
    if user_id is None:
        return (jsonify({"error": "Missing user_id"}), 400)

    my_user = storage.get("User", user_id)
    if my_user is None:
        abort(404)

    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_place = Place()
    new_place.city_id = my_city.id

    for key, val in content.items():
        setattr(new_place, key, val)

    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    '''Updates a place based on its id'''

    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)

    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    not_allowed = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_place, key, value)
    my_place.save()

    return (jsonify(my_place.to_dict()), 200)
