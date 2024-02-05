#!/usr/bin/python3
"""
Contains the places_reviews view for the AirBnB clone v3 API.
Handles all default RESTful API actions for Review objects related to Places.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews_for_place(place_id):
    """Retrieves all Review objects for a specified Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Not found')
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a specific Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404, 'Not found')
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review for a specified Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Not found')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, 'User not found')
    if 'text' not in data:
        abort(400, 'Missing text')
    review = Review(place_id=place_id, **data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404, 'Not found')
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a specific Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404, 'Not found')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
