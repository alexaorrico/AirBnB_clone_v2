#!/usr/bin/python3
"""This module implement a rule that return a view"""
from api.v1.views import app_views, Review, Place, User, storage
from flask import abort, jsonify, request

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Get a list of all reviews for a specific Place."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get a Review object by its ID."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object by its ID."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new Review for a Place."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return "Not a JSON", 400
    if 'user_id' not in data:
        return "Missing user_id", 400
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        return "Missing text", 400
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object by its ID."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return "Not a JSON", 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
