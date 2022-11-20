#!/usr/bin/python3
"""Contains function that handles all requests to the /amenities endpoints."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import amenity, storage


@app_views.route("/amenities",
                 strict_slashes=False,
                 defaults={'amenity_id': None},
                 methods=['GET', 'POST', 'PUT'])
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def amenities_endpoint(amenity_id):
    """Handle all requests to the /amenities endpoints."""
    if request.method == "GET":
        if amenity_id is None:
            return [obj.to_dict() for obj in storage.all(amenity.Amenity).values()]
        elif amenity_id is not None:
            am_obj = storage.get("Amenity", amenity_id)
            if not am_obj:
                abort(404)
            return jsonify(obj.to_dict())
    elif request.method == "POST":
        try:
            post_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        if 'name' not in post_data:
            return make_response("Missing name", 400)
        new_amenity = amenity.Amenity()
        new_amenity.name = post_data['name']
        new_amenity.save()
        return make_response(new_amenity.to_dict(), 201)
    elif request.method == "PUT":
        try:
            put_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        am_obj = storage.get("Amenity", amenity_id)
        if not am_obj:
            abort(404)
        for key, value in put_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(am_obj, key, value)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    elif request.method == "DELETE":
        am_obj = storage.get("Amenity", amenity_id)
        if am_obj is None:
            abort(404)
        am_obj.delete()
        storage.save()
        return (jsonify({}))
