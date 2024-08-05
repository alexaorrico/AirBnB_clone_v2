#!/usr/bin/python3
"""
Module for handling review-related API endpoints
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """
    Retrieve all reviews associated with a specific place.
    Returns a list of reviews in JSON format.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    response = [review.to_dict() for review in place.reviews]
    return jsonify(response)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieve a specific review by its ID.
    Returns the review details in JSON format.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete a specific review by its ID.
    Returns an empty response with a 200 status code if successful.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Create a new review for a specific place.
    Requires 'text' and 'user_id' in the request body.
    Returns the created review in JSON format with a 201 status code.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if not isinstance(body, dict):
        abort(400, 'Not a JSON')
    if 'text' not in body:
        abort(400, 'Missing text')
    if 'user_id' not in body:
        abort(400, 'Missing user_id')
    if storage.get(User, body['user_id']) is None:
        abort(400, 'Invalid user_id')
    body['place_id'] = place_id
    review = Review(**body)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Update an existing review by its ID.
    Updates fields provided in the request body.
    Returns the updated review in JSON format.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    new_data = request.get_json()
    if not isinstance(new_data, dict):
        abort(400, 'Not a JSON')
    for key, value in new_data.items():
        if key not in [
            'id',
            'created_at',
            'place_id',
            'user_id',
                'updated_at']:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
