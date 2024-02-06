#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort, request
from models import storage
from models.state import State
from models.city import City
from models.base_model import BaseModel


@app_views.route('/amenities', methods=["GET"],
                 strict_slashes=False)
def get_amenities():
    res = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        res.append(amenity.to_dict())
    return jsonify(res)


@app_views.route('/amenities', methods=["GET", "POST"],
                 strict_slashes=False)
def create_amenity():
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    amenity = State(**request.json)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=[
                 "GET", "PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
        if request.method == "PUT":
            if not request.json:
                abort(400, description="Not a JSON")
            for key, value in request.json.items():
                setattr(amenity, key, value)
            amenity.save()
            return (jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities():
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)
