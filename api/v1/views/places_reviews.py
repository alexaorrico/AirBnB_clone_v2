#!/usr/bin/python3
"""
This module defines a Flask web application that
provides a RESTful API for Review objects.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
    """
    place = next((place for place in storage.all(Place).values()
                 if place.id == place_id), None)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in storage.all(Review).values()
               if review.place_id == place_id]
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object.
    """
    review = next((review for review in storage.all(Review).values()
                  if review.id == review_id), None)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object.
    """
    review = next((review for review in storage.all(Review).values()
                  if review.id == review_id), None)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review.
    """
    place = next((place for place in storage.all(Place).values()
                 if place.id == place_id), None)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = next((user for user in storage.all(User).values()
                if user.id == data['user_id']), None)
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object.
    """
    review = next((review for review in storage.all(Review).values()
                  if review.id == review_id), None)
    if review is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
