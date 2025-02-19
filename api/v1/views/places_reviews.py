#!/usr/bin/python3
"""
Review objects API routes
"""

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400

    new_review = Review(place_id=place_id, **data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    # Ignoring keys that should not be updated
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
