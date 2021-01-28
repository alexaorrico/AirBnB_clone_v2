#!/usr/bin/python3
"""view for Review object that handles all default RestFul API actions
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_of_place(place_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_place = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_place)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a specific review object """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """Deletes a review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a review object"""
    if request.get_json() is None:
        return "Not a JSON", 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if 'user_id' not in request.get_json():
        return "Missing user_id", 400
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        return "Missing text", 400

    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def Update_review(review_id):
    """Update a review store in the storage"""
    if request.get_json() is None:
        return "Not a JSON", 400
    review = storage.get(Review, review_id)
    if review:
        ignore_keys = ['id', 'user_id', 'place_id' 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
