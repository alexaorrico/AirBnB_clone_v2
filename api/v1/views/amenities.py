#!/usr/bin/python3
"""
Amenity
"""

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities/', methods=["GET"])
@app_views.route('/amenities', methods=["GET"])
def amenities():
    """GET All amenities"""
    amenities = storage.all(Amenity).values()
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return (jsonify(amenity_list))


@app_views.route('/amenities/<string:id>/', methods=["GET"])
@app_views.route('/amenities/<string:id>', methods=["GET"])
def amenities_by(id):
    """GET Amenity by id"""
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route('/amenities/<string:id>/', methods=["DELETE"])
@app_views.route('/amenities/<string:id>', methods=["DELETE"])
def remove_amenities(id):
    """REMOVE by id"""
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route('/amenities/', methods=["POST"])
@app_views.route('/amenities', methods=["POST"])
def create_amenities():
    """CREATE Amenity"""
    if request.is_json:
        amenities_json = request.get_json()
        if amenities_json.get("name") is None:
            abort(400, description="Missing name")
        else:
            new_amenity = Amenity(**amenities_json)
            storage.new(new_amenity)
            storage.save()
            return new_amenity.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/amenities/<string:id>', methods=["PUT"])
def update_amenities(id):
    """UPDATE Amenity by id"""
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    if request.is_json:
        forbidden = ["id", "created_at", "updated_at"]
        amenities_json = request.get_json()
        storage.delete(amenity)
        for k, v in amenities_json.items():
            if amenities_json[k] not in forbidden:
                setattr(amenity, k, v)
        storage.new(amenity)
        storage.save()
        return amenity.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
