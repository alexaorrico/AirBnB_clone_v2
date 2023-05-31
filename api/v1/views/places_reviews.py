#!/usr/bin/python3
"""restful API functions for Place"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route(
        "/places/<place_id>/reviews", strict_slashes=False,
        methods=["GET", "POST"])
def places_end_points(place_id):
    """place objects that handles all default RESTFul API actions"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == "GET":
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews), 200

    elif request.method == "POST":
        data = request.get_json()
        if not data or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if not data.get("user_id"):
            abort(400, "Missing user_id")
        if not data.get("text"):
            abort(400, "Missing text")
        user = storage.get(User, data["user_id"])
        if not user:
            abort(404)
        data["place_id"] = place_id
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>", strict_slashes=False,
        methods=["DELETE", "PUT", "GET"])
def review_end_points(review_id):
    """place objects that handles all default RESTFul API actions"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data or not isinstance(data, dict):
            abort(400, "Not a JSON")
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
