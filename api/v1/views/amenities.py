#!/usr/bin/python3
"""this view hundles states endpoints"""
from flask import abort
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify
from flask import request
from flask import make_response
from models.state import State
from models import storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenity():
    """gets all amenities instances"""
    d_amen = storage.all(Amenity)
    ama_l = []
    for ama in d_amen.values():
        ama_l.append(ama.to_dict())
    return jsonify(ama_l)


@app_views.route("/amenities/<amenities_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenities_id):
    """gets amenity with the given id"""
    d_amen = storage.get(Amenity, amenities_id)
    if d_amen:
        return jsonify(d_amen.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenities_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenities_id):
    """deletes amenity with the given id"""
    d_amen = storage.get(Amenity, amenities_id)
    if d_amen:
        storage.delete(d_amen)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """create new amenity with the supplied data"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if "name" not in data:
        return make_response(jsonify({"error": "Name required"}), 400)
    new = Amenity(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/amenities/<amenities_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenities_id):
    """updates amenities with supplied id"""
    d_amen = storage.get(Amenity, amenities_id)

    if not d_amen:
        abort(404)

    if request.get_json():
        data = request.get_json()
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(d_amen, k, v)
        d_amen.save()
        return make_response(jsonify(d_amen.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
