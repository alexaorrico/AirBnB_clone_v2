#!/usr/bin/python3
"""
Module Places_Reviews
"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = place.reviews
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieves a Review object by ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    content = request.get_json()
    if content is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in content:
        return jsonify({'error': 'Missing user_id'}), 400

    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)

    if 'text' not in content:
        return jsonify({'error': 'Missing text'}), 400

    content['place_id'] = place_id
    new_review = Review(**content)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object by ID
    """
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    content = request.get_json()
    if content is None:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in content.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
