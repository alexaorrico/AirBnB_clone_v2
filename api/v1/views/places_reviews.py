#!/usr/bin/python3
"""
Reviews API
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'],
        strict_slashes=False)
def get_reviews(place_id):
    """Retrive all reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route(
        '/reviews/<review_id>', methods=['GET'],
        strict_slashes=False)
def get_review(review_id):
    """Retrive a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'],
        strict_slashes=False)
def del_review(review_id):
    """Delete the review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'],
        strict_slashes=False)
def create_review(place_id):
    """Create a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review = request.get_json()
    if type(review) != dict:
        abort(400, "Not a JSON")
    if "user_id" not in review:
        abort(400, "Missing user_id")
    user = storage.get(User, review["user_id"])
    if not user:
        abort(404)
    if "text" not in review:
        abort(400, "Missing text")

    review['place_id'] = place_id
    review = Review(**review)
    # review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>', methods=['PUT'],
        strict_slashes=False)
def update_review(review_id):
    """Update review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    res = request.get_json()
    if not res:
        abort(400, "Not a JSON")
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for item in res:
        if item not in ignore:
            setattr(review, item, res[item])
    storage.save()
    return jsonify(review.to_dict()), 200
