#!/usr/bin/python3
"""
place review view api
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    retrieves all reviews of a place
    """
    place = storage.get(Place, place_id)
    if place:
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    abort(404)


@app_views.route('reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    retrieve a review object
    """
    review = storage.get(Review, review_id)
    if review:
        response = review.to_dict()
        return jsonify(response)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    deletes a review object
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    create a review for a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json()
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, "Missing text")

    review = Review(**data)
    review.save()
    response = review.to_dict()
    return jsonify(response), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    updates an review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_attributes = [
        'id', 'user_id', 'place_id', 'created_at', 'updated_at'
    ]
    for attribute, value in data.items():
        if attribute not in ignore_attributes:
            setattr(review, attribute, value)
    review.save()
    response = review.to_dict()
    return jsonify(response), 200
