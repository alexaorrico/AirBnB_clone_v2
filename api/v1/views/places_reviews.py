#!/usr/bin/python3
"""Defines all the places_reviews routes"""

from flask import jsonify, request, abort
from api.v1.views import reviews_view
from models import storage, Place, Review


@reviews_view.route('/places/<place_id>/reviews', methods=['GET'], 
                    strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = storage.all(Review).values()
    place_reviews = [review.to_dict() for review in reviews if 
                     review.place_id == place_id]

    return jsonify(place_reviews)


@reviews_view.route('/reviews/<review_id>', methods=['GET'], 
                          strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@reviews_view.route('/reviews/<review_id>', methods=['DELETE'], 
                          strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    review.delete()
    storage.save()

    return jsonify({}), 200


@reviews_view.route('/places/<place_id>/reviews', methods=['POST'], 
                          strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    user_id = data.get('user_id')
    if user_id is None:
        abort(400, description="Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    text = data.get('text')
    if text is None:
        abort(400, description="Missing text")

    new_review = Review(place_id=place_id, user_id=user_id, text=text)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@reviews_view.route('/reviews/<review_id>', methods=['PUT'], 
                          strict_slashes=False)
def update_review(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200
