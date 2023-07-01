#!/usr/bin/python3
"""View for Review objects that handles default API actions."""
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieve the list of all Review objects of a Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    is_review = []

    for review in place.reviews:
        is_review.append(review.to_dict())
    return jsonify(is_review)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new Review."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")

    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "text" not in data:
        abort(400, "Missing text")

    review = Review(**data)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
