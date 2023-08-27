#!/usr/bin/python3
""" View for Reviews """

from flask import jsonify, request, abort
from models import Place, Review, User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects for a specific Place"""
    place = Place.query.get(place_id)
    if not place:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a specific Review object by its ID"""
    review = Review.query.get(review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific Review object by its ID"""
    review = Review.query.get(review_id)
    if not review:
        abort(404)
    review.delete()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object for a specific Place"""
    place = Place.query.get(place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = User.query.get(data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")
    review = Review(place_id=place_id, user_id=data['user_id'], **data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a specific Review object by its ID"""
    review = Review.query.get(review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    keys_to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
