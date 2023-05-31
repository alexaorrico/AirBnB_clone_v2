#!/usr/bin/python3

"""
a new view for State objects that handles all default RESTFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def retrieve_place(city_id):
    """
    Retrieves all places linked to a city
    """

    place_list = []
    city = storage.get(City, city_id)
    if city:
        for i in city.places:
            place_list.append(i.to_dict())
        return jsonify(place_list)
    abort(404)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_place_using_placeid(place_id):
    """
    REtrieves the place using the place id
    Raises a 404 error if the place_id isnt linked to a place
    """

    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_using_placeid(place_id):
    """
    Deletes a placee using the place id
    Raises a 404 error If the place_id is not linked to any Place object
    Returns an empty dictionary with the status code 200
    """

    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/cities/city_id/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
    Posts a new place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    place_data = request.get_json()
    place_data['city_id'] = city_id
    place = Place()
    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)
    for key, value in place_data.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a place  using the place id
    Returns a 404 error if the place id is not linked to any place
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = storage.get(Place, place_id)
    keys_ignore = ["id", "user_id", "city_id", "updated_at", "created_at"]
    if place:
        for key, value in request.get_json().items():
            if key not in keys_ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(404)
