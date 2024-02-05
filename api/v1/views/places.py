#!/usr/bin/python3
"""a module as places API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    """a function to retrieve all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>")
def get_place(place_id):
    """a function to get a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    """a function to delete a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """a function to create a new Place in a City object"""
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in json_req:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in json_req:
        return jsonify({"error": "Missing name"}), 400

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_req['city_id'] = city_id

    user_id = json_req['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    place = Place(**json_req)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'])
def update_place(place_id):
    """a function to update a Place object"""
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in json_req.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
