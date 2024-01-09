#!/usr/bin/python3
"""Handles all RESTful API actions for `place_reviews` relationship"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, request, abort


@app_views.route("/places/<place_id>/reviews")
def reviews_of_a_place(place_id):
    """Get all reviews of a place.

    Args:
        place_id (str): ID of the place to get the reviews from.

    Returns:
        list: Reviews of that place.

    Raises:
        404: If the specified place_id does not exist.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    result = []

    for review in place.reviews:
        result.append(review.to_dict())

    return jsonify(result)


@app_views.route("/reviews/<review_id>")
def review(review_id):
    """Get a review.

    Args:
        review_id (str): ID of the review.

    Returns:
        dict: Review in JSON.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Remove a review.

    Args:
        review_id (str): ID of the review.

    Returns:
        dict: An empty JSON.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Create a review.

    Args:
        place_id (str): ID of the place to review.

    Returns:
        dict: The created review.

    Raises:
        404: If the specified place_id or user_id does not exist
        400: If the request body is not a valid JSON or if it is missing
             user_id or text.
    """
    place = storage.get(Place, place_id)
    payload = request.get_json()
    if not place:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    if not storage.get(User, payload["user_id"]):
        abort(404)
    if "text" not in payload:
        abort(400, "Missing text")

    review = Review(place_id=place_id, **payload)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Update a review.

    Args:
        review_id (str): ID of the review to update.

    Returns:
        dict: The updated review.

    Raises:
        404: If the specified review_id does not exist
        400: If the request body is not a valid JSON.
    """
    review = storage.get(Review, review_id)
    payload = request.get_json()
    if not review:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")

    for key, value in review.to_dict().items():
        if key not in [
            "id",
            "user_id",
            "place_id",
            "created_at",
            "updated_at",
            "__class__",
        ]:
            setattr(review, key, payload[key] if key in payload else value)
    review.save()

    return jsonify(review.to_dict())
