#!/usr/bin/python3
""" Create a view for the Place Objects """


from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/places", methods=["GET"])
def all_places():
    """ Retrieve all Place objects """
    places = storage.all(Place)
    place_list = [place.to_dict() for place in places.values()]
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=["GET"])
def one_place(place_id):
    """ Retrieves a Place Object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """ Retrieves a Place Object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route("/cities/<city_id>", methods=["POST"])
def create_place(city_id):
    """ Create a new Place object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(name=data["name"], user_id=data["user_id"])

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """ Update a Place object """
    one_place = storage.get(Place, place_id)

    if not one_place:
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(one_place, key, value)

    storage.save()
    return jsonify(one_place.to_dict()), 200
