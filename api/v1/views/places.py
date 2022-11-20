#!/usr/bin/python3
"""Contain functions that handle all requests to the /places endpoint."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import city, place, storage, user


@app_views.route("/places", strict_slashes=False,
                 defaults={'place_id': None},
                 methods=['GET', 'PUT'])
@app_views.route("/places/<place_id>",  methods=['GET', 'DELETE', 'PUT'])
def get_place(place_id):
    """Handles get, delete, put request to the places endpoint"""
    if request.method == "GET":
        if place_id is None:
            return [obj.to_dict() for obj in storage.all(place.Place).values()]
        elif place_id is not None:
            pl_obj = storage.get("Place", place_id)
            if not pl_obj:
                abort(404)
            return jsonify(pl_obj.to_dict())
    elif request.method == "PUT":
        try:
            put_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        pl_obj = storage.get("Place", place_id)
        if not pl_obj:
            abort(404)
        for key, value in put_data.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(pl_obj, key, value)
        pl_obj.save()
        return make_response(jsonify(pl_obj.to_dict()), 200)
    elif request.method == "DELETE":
        pl_obj = storage.get("Place", place_id)
        if pl_obj is None:
            abort(404)
        pl_obj.delete()
        storage.save()
        return (jsonify({}))

@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=["GET"])
def get_city_places(city_id):
    """Handles get requests to city places endpoint."""
    ci_obj = storage.get("City", city_id)
    if not ci_obj:
        abort(404)
    return [place for place in storage.all(place.Place).values()\
            if place.city_id == city_id]


@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=["POST"])
def post_place(city_id):
    """Handles post requests to city places endpoint."""
    ci_obj = storage.get("City", city_id)
    if not ci_obj:
        abort(404)
    try:
        post_data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if 'user_id' not in post_data:
        return make_response("Missing user_id", 400)
    u_obj = storage.get("User", post_data.get("user_id"))
    if not u_obj:
        abort(404)
    if "name" not in post_data:
        return make_response("Missing name", 400)
    new_place = place.Place()
    new_place.city_id = city_id
    new_place.name = post_data['name']
    new_place.user_id = post_data['user_id']
    new_place.city_id = city_id
    new_place.save()
    return make_response(new_place.to_dict(), 201)
