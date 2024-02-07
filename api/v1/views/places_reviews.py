#!/usr/bin/python3
"""Handles all RESTful API actions for place_reviews relationship"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def reviews_of_a_place(place_id):
    """Get all reviews of a place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    result = [review.to_dict() for review in place.reviews]
    return jsonify(result)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def review(review_id):
    """Get a review."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Remove a review."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Create a review."""
    place = storage.get(Place, place_id)
    payload = request.get_json()
    if not place or not payload or "user_id" not in payload or \
            "text" not in payload:
        abort(400)

    user_id = payload["user_id"]
    if not storage.get(User, user_id):
        abort(404)

    review = Review(place_id=place_id, **payload)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Update a review."""
    review = storage.get(Review, review_id)
    payload = request.get_json()
    if not review or not payload:
        abort(404)

    for key, value in payload.items():
        if key != "id" and key != "user_id" and key != "place_id" \
                and key != "created_at" and key != "updated_at" \
                and hasattr(review, key):
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict())
