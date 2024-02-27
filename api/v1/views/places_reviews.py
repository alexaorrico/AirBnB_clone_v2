#!/usr/bin/python3
"""
view for Review object that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_cities(place_id):
    """Retrieves the list of all Review objects of a Place"""
    review_obj = storage.get("Review", str(place_id))
    if review_obj is None:
        abort(404)
    all_reviews = review_obj.cities
    result = [review.to_dict() for review in all_reviews]
    return jsonify(result), 200


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_city(review_id):
    """etrieves a Review object"""
    review_obj = storage.get("Review", str(review_id))
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(review_id):
    """Deletes a Review object"""
    review_obj = storage.get("Review", str(review_id))
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return ({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_city(place_id):
    """Creates a Review"""
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, "Not a JSON")
    if "text" not in review_json:
        abort(400, "Missing text")
    if "user_id" not in review_json:
        abort(400, "Missing user_id")
    review_json["place_id"] = place_id
    review_inst = City(**review_json)
    review_inst.save()
    return jsonify(review_inst.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_city(review_id):
    """pdates a Review object"""
    review_obj = storage.get("City", str(review_id))
    review_json = request.get_json(silent=True)
    if review_obj is None:
        abort(404)
    if review_json is None:
        abort(400, "Not a JSON")
    for k, value in review_json.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review_obj, k, value)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
