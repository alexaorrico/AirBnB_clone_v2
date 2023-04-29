#!/usr/bin/python3
"""Creates a view for Review objects"""

import json
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReviews(place_id):
    """gets all the reviews associated with the place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in storage.all(Review).values()
               if review.place_id == place_id]
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getReview(review_id):
    """gets a single review based on it's id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    """deletes a review from db"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def addReview(place_id):
    """adds a new review to the db with place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    obj = request.get_json()

    if 'user_id' not in obj:
        abort(400, "Missing user_id")

    user_id = obj['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'text' not in obj:
        abort(400, "Missing text")

    obj['place_id'] = place_id
    review = Review(**obj)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    """updates a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
