#!/usr/bin/python3
"""
Amenity view
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Retrieves all amenity objects from a specific id"""
    amenity_obj = storage.get("Amenity", amenity_id)

    if amenity_obj is None:
        abort(404)

    return jsonify(amenity_obj.to_dict())


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def city_create():
    """Creates a Amenity """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')

    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    resp = jsonify(new_amenity.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amentiy():
    """Gets all amenity objects"""
    amenity_list = []
    fetched_obj = storage.all("Amenity")

    if fetched_obj is None:
        abort(404)

    for obj in fetched_obj.values():
        amenity_list.append(obj.to_dict())

    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def city_put(amenity_id):
    """Updates a specific amenity object by ID"""
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Amenity", str(amenity_id))
    if fetched_obj is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(amenity_id):
    """Deletes Amenity by ID"""
    fetched_obj = storage.get("Amenity", str(amenity_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
