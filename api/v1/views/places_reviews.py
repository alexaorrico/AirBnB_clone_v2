#!/usr/bin/python3

"""Handles APIs for places_review"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, Review, User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_place(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    reviews = [r.to_dict() for r in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    my_dict = request.get_json()
    user_id = my_dict.get('user_id')
    if not user_id:
        abort(400, 'Missing user_id')
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    text = my_dict.get('text')
    if not text:
        abort(400, 'Missing text')
    review = Review(user_id=user_id, place_id=place_id, text=text)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    my_dict = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
