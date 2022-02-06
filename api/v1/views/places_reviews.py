#!/usr/bin/python3
"""view for review objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models import review
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all reviews given an place"""
    reviews_list = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('reviews/<review_id>', strict_slashes=False)
def review_by_id(review_id):
    """Retrieves a review by a given ID"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    'reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_review(review_id):
    """Deletes a review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False
    )
def create_review(place_id):
    """Creates a review object"""
    request_data = request.get_json()
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request_data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', request_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request_data:
        return jsonify({"error": "Missing text"}), 400
    text = request.get_json().get('text')
    user_id = request.get_json().get('user_id')
    obj = Review(text=text, user_id=user_id, place_id=place_id)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
