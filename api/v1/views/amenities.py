#!/usr/bin/python3
"""
Module contains all endpoints to GET, POST, PUT OR DELETE
objects from Amenity model.
"""


from models import storage
from models.amenity import Amenity
from flask import jsonify
from api.v1.views import app_views
from flask import abort
from flask import request
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    objs = storage.all(Amenity).values()
    amenities = [obj.to_dict() for obj in objs]
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieves a Amenity object by id.
    """
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Deletes a Amenity object by id.
    """
    obj = storage.get(Amenity, amenity_id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity_obj():
    """
    Creates a new Amenity object.
    """
    try:
        body = request.get_json()
    except Exception:
        raise BadRequest("Not a JSON")

    if "name" not in body.keys():
        raise BadRequest("Missing name")
    obj = Amenity(name=body.get("name"))
    storage.new(obj)
    storage.save()
    amenity = storage.get(Amenity, obj.id)
    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity_obj(amenity_id):
    """
    Updates a Amenity object.
    """
    try:
        body = request.get_json()
    except Exception:
        raise BadRequest("Not a JSON")

    for key in body.keys():
        if key not in dir(Amenity):
            msg = "Attribute {} not found in Amenity object".format(key)
            raise BadRequest(msg)

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        raise NotFound()

    new_name = body.get("name")
    amenity_obj.name = new_name
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
