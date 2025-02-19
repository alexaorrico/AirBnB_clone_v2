#!/usr/bin/python3
"""
Module for Places review
"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_all_reviews(place_id):
    """  Method retrieve list of all Reviews"""
    place = storage.get('Place', place_id)
    if place:
        reviews = place.reviews
        return jsonify([review.to_dict() for review in reviews])
    else:
        return abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """ Method to retrieve a Review """
    review = storage.get('Review', review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        return abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete review """
    review = storage.get('Review', review_id)

    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """POST to make changes to reviews"""

    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    review = request.get_json()
    if not review:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in review:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in review:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    user_id = review.get("user_id")
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    fresh_review = Review(**review)
    fresh_review.place_id = place.id
    fresh_review.user_id = user.id
    storage.new(fresh_review)
    storage.save()

    return jsonify(fresh_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update Review"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    review = storage.get('Review', review_id)
    if not review:
        return abort(404)

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict())
