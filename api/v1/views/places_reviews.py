#!/usr/bin/python3
"""import modules
"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrives Reviews
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route(
        '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrive a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """create a Review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in data:
        abort(400, "Missing text")

    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>', methods=['POST'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
