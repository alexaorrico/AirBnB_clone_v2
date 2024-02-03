#!/usr/bin/python3
"""
This is the module for places
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    "/api/v1/cities/<city_id>/places", methods=["GET"], strict_slashes=False
)
def all_places(city_id):
    """Retrieves the list of all City objects of a State"""
    obj_city = storage.get(City, city_id)
    if not obj_city:
        abort(404)

    places = [obj.to_dict() for obj in obj_city.places]
    return jsonify(places)


@app_views.route("/api/v1/places/<place_id>", methods=["GET"], strict_slashes=False)
def one_place(place_id):
    """Retrieves a City object"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/api/v1/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def del_city(place_id):
    """Returns an empty dictionary with status code 200"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/api/v1/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Creates one city with the state_id given"""
    obj_state = storage.get(City, city_id)
    if not obj_state:
        abort(404)

    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")

    user_id = new_place["user_id"]
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    if "name" not in new_place:
        abort(400, "Missing name")

    obj = Place(**new_place)
    setattr(obj, "city_id", city_id)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates one city tied with the given state_id"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)

    rq = request.get_json()
    if not rq:
        abort(400, "Not a JSON")

    for key, value in rq.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(obj, key, value)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
