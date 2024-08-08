#!/usr/bin/python3
"""modify place objects via APIs"""
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, make_response, abort, request
from models import storage
from api.v1.views import app_views


def abortNotExists(cls, obj_id):
    """exit with a 404 status if obj not found"""
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["GET"])
def get_city_places(city_id=None):
    """Retrieves the list of all Place objects of a City:
       GET /api/v1/cities/<city_id>/places
    """
    city = abortNotExists(City, city_id)
    places_dicts_list = []
    for place in city.places:
        places_dicts_list.append(place.to_dict())
    return jsonify(places_dicts_list)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET"])
def get_places(place_id):
    """Retrieves a Place object. : GET /api/v1/places/<place_id>"""
    obj = abortNotExists(Place, place_id)
    return jsonify(obj.to_dict())


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["POST"])
def post_places(city_id):
    """create a new place object"""
    abortNotExists(City, city_id)
    try:
        data = request.get_json()
        data["city_id"] = city_id
    except Exception:
        abort(400, description="Not a JSON")
    if "user_id" not in data.keys():
        abort(400, description="Missing user_id")

    abortNotExists(User, data["user_id"])  # check for user id if it exists
    if "name" not in data.keys():
        abort(400, description="Missing name")
    new_obj = Place(**data)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """Deletes a Place object: DELETE /api/v1/places/<place_id>"""
    obj = abortNotExists(Place, place_id)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def put_place(place_id):
    """Updates a place object: PUT /api/v1/places/<place_id>"""
    obj = abortNotExists(Place, place_id)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(obj, key, val)

    storage.save()
    return make_response(obj.to_dict(), 200)
