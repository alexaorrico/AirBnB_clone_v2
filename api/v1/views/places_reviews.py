#!/usr/bin/python3
""" new view for places_review objects"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, Review, User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object for a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if "text" not in data:
        abort(400, description="Missing text")
    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
