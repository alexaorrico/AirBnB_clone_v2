#!/usr/bin/python3
"""
a new view for Review objects that handles all default RESTFul API actions.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review_by_id(review_id):
    """
    Retrieves, updates, or deletes a Review object by ID.

    GET /api/v1/reviews/<review_id> - Retrieves a Review object.
    PUT /api/v1/reviews/<review_id> - Updates a Review object.
    DELETE /api/v1/reviews/<review_id> - Deletes a Review object.

    Args:
    review_id (str): ID of the Review.

    Returns:
    JSON: Review obj or success message.
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_by_place(place_id):
    """
    Retrieves the list of all Review obj of a Place or creates a new Review.

    GET /api/v1/places/<place_id>/reviews - Retrieves reviews of a place.
    POST /api/v1/places/<place_id>/reviews - Creates a new Review.

    Args:
    place_id (str): ID of the Place.

    Returns:
    JSON: List of Review objects or newly created Review.
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        if 'text' not in data:
            abort(400, 'Missing text')

        user_id = data['user_id']
        user = storage.get(User, user_id)

        if user is None:
            abort(400)

        new_review = Review(**data)
        new_review.place_id = place_id
        new_review.save()
        return jsonify(new_review.to_dict()), 201
