#!/usr/bin/python3
"""
Route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieves all Place objects by city
    :return: JSON of all Places
    """
    list_of_places = []
    obj_city = storage.get("City", str(city_id))
    for obj in obj_city.places:
        list_of_places.append(obj.to_json())

    return jsonify(list_of_places)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create place route
    :return: Newly created Place object
    """
    places_json = request.get_json(silent=True)
    if places_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", places_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in places_json:
        abort(400, 'Missing user_id')
    if "name" not in places_json:
        abort(400, 'Missing name')

    places_json["city_id"] = city_id

    new_place = Place(**places_json)
    new_place.save()
    rsponse = jsonify(new_place.to_json())
    rsponse.status_code = 201

    return rsponse


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Gets a specific Place object by ID
    :param place_id: Place object ID
    :return: Place object with the specified ID or error
    """

    obj_fetched = storage.get("Place", str(place_id))

    if obj_fetched is None:
        abort(404)

    return jsonify(obj_fetched.to_json())


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates specific Place object by ID
    :param place_id: Place object ID
    :return: Place object and 200 on success, or 400 or 404 on failure
    """
    places_json = request.get_json(silent=True)

    if places_json is None:
        abort(400, 'Not a JSON')

    obj_fetched = storage.get("Place", str(place_id))

    if obj_fetched is None:
        abort(404)

    for key, val in places_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(obj_fetched, key, val)

    obj_fetched.save()

    return jsonify(obj_fetched.to_json())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """
    Deletes Place by ID
    :param place_id: Place object ID
    :return: Empty dict with 200 or 404 if not found
    """

    obj_fetched = storage.get("Place", str(place_id))

    if obj_fetched is None:
        abort(404)

    storage.delete(obj_fetched)
    storage.save()

    return jsonify({})
