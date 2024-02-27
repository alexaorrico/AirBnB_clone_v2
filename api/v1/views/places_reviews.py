#!/usr/bin/python3
"""Review View"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, Review, User


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'text' not in request.json:
        abort(400, 'Missing text')
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    review = Review(**request.json)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
