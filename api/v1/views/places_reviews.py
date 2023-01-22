#!/usr/bin/python3
"""
place reviews view routes
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    "/places/<place_id>/reviews",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def place_reviews(place_id):
    """Handles /places/<place_id>/reviews endpoint

    Returns:
        json: list of all reviews for a place or the newly added review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "POST":
        review_data = request.get_json(silent=True)
        if review_data is None:
            return jsonify(error="Not a JSON"), 400

        if "user_id" not in review_data:
            return jsonify(error="Missing user_id"), 400
        elif "text" not in review_data:
            return jsonify(error="Missing text"), 400
        else:
            user = storage.get(User, review_data["user_id"])
            if user is None:
                abort(404)
            review_data["place_id"] = place.id
            review = Review(**review_data)
            storage.new(review)
            storage.save()
            return jsonify(review.to_dict()), 201
    else:
        return jsonify([review.to_dict() for review in place.reviews])


@app_views.route(
    "/reviews/<review_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def reviews(review_id):
    """Handles /reviews/<review_id> endpoint

    Returns:
        json: review or empty dict
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        review_data = request.get_json(silent=True)
        if review_data is None:
            return jsonify(error="Not a JSON"), 400

        for key, value in review_data.items():
            if key not in [
                    "id", "user_id", "place_id", "created_at", "updated_at"
            ]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())

    else:
        return jsonify(review.to_dict())
