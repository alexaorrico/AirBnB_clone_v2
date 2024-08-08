#!/usr/bin/python3
"""modify Amenity objects via APIs"""
from models.amenity import Amenity
from flask import jsonify, make_response, abort, request
from models import storage
from api.v1.views import app_views


def abortNotExists(cls, obj_id):
    """exit with a 404 status if obj not found"""
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["GET"])
def get_amenities(amenity_id=None):
    """retrieve Amenity objects"""
    if not amenity_id:
        objs_dict = storage.all(Amenity)
        obj_list = []
        for obj in objs_dict.values():
            obj_list.append(obj.to_dict())
        return make_response(jsonify(obj_list))

    else:
        obj = abortNotExists(Amenity, amenity_id)
        return make_response(jsonify(obj.to_dict()))


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenities():
    """create a new amenity object"""
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")

    new_obj = Amenity(**data)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """DELETE /api/v1/amenities/<amenity_id>"""
    obj = abortNotExists(Amenity, amenity_id)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["PUT"])
def put_amenity(amenity_id):
    """Updates a amenity_id object: PUT /api/v1/amenities/<amenity_id>"""
    obj = abortNotExists(Amenity, amenity_id)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, val)

    storage.save()
    return make_response(obj.to_dict(), 200)
