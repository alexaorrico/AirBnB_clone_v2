#!/usr/bin/python3
"""
Places View
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views('/cities/<city_id>/places', methods=["GET"],
           strict_slashes=False)
def get_places(city_id):
    """Gets all Places by using City ID"""
    fecthed_city = storage.get("City", str(city_id))
    if fecthed_city is None:
        abort(404)

    places_list = []
    for obj in fecthed_city.places:
        places_list.append(obj.to_dict())

    resp = jsonify(places_list)
    return resp


@app_views('/places/<place_id>', methods=['GET'],
           strict_slashes=False)
def get_place(place_id):
    """Gets place using an ID"""
    fetched_place = storage.get('Place', str(place_id))
    if fetched_place is None:
        abort(404)
    resp = jsonify(fetched_place.to_dict())
    return resp


@app_views('/places/<place_id>', methods=['DELETE'],
           strict_slashes=False)
def delete_place(place_id):
    """Deletes a place based on the ID"""
    fetched_place = storage.get("Place", str(place_id))
    if fetched_place is None:
        abort(404)
    storage.delete(fetched_place)
    storage.save()
    return ({}, 200)


@app_views('/cities/<city_id>/places', methods=['POST'],
           strict_slashes=False)
def create_place(city_id):
    """Creates a place using cit ID"""
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("City", str(city_id)):
        abort(404)

    if not storage.get("User", place_json["user_id"]):
        abort(404)

    if "name" not in place_json:
        abort(400, 'Missing name')

    if "user_id" not in place_json:
        abort(400, "Missing user_id")

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_dict())
    resp.status_code = 201

    return resp


@app_views('/places/<place_id>', methods=['PUT'],
           strict_slashes=False)
def updates_place(place_id):
    """Updates a Place"""
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404)
    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())
