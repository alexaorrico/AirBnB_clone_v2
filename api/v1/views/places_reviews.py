#!/usr/bin/python3
"""
Module for handling RESTful API actions for Review objects.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import *
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")

    reviews = storage.all(Review).values()
    place_reviews = [review.to_dict() for review in reviews
                      if review.place_id == place_id]
    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description=f"Review with ID {review_id} not found")
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description=f"Review with ID {review_id} not found")

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404, description=f"User with ID {data['user_id']} not found")

    new_review = Review(place_id=place_id, **data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description=f"Review with ID {review_id} not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
