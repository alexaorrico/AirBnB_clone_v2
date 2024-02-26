#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, User, Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a Review."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    data = request.get_json
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")
    user_id = data['user_id']
    if storage.get(User, user_id) is None:
        abort(404)
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    data = request.get_json
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
