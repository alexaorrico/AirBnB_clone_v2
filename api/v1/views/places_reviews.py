#!/usr/bin/python3
"""places_reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
from models.user import User
import uuid


@app_views.route(
    '/places/<place_id>/reviews', mathods=['GET'], strict_slashes=False
)
def get_reviews_by_place(place_id):
    """ Get the review by the place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

# Route for retirivng a specifc Review obj by ID


@app_views.route(
    '/reviews/<review_id>', methods=['GET'], strict_slashes=False
)
def get_review(review_id):
    """ Get the review by review id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)

# Route to DELETE the review


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False
)
def delete_review(review_id):
    """Delte the review by the ID"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

# Route to create a new review


@app_views.route(
    '/places/<place_id>/reviews', methods=['PSOT'], strict_slashes=False
)
def create_review(place_id):
    """ Create new Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    if 'text' not in data:
        abort(400, "Missing text")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(400)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201

# Route to update the review


@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False
)
def update_review(review_id):
    """ Update the review"""
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, "Not a JSON")

        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in ignore_keys:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
