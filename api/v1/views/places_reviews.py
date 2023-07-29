#!/usr/bin/python3
"""review obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_in_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    places_list = [review.to_dict() for review in place.reviews]
    return jsonify(places_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id=None):
    """Get all reviews or a reviews whose id is specified"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = request.get_json()
    if not review:
        abort(400, description="Not a JSON")
    if 'user_id' not in review:
        abort(400, description="Missing user_id")
    user = storage.get(User, review.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in review:
        abort(400, description="Missing text")
    review['place_id'] = place_id
    obj = Review(**review)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Update a review object"""
    review = storage.get(Review, review_id)
    fixed_data = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in fixed_data:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
