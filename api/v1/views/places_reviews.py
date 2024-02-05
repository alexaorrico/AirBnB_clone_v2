#!/usr/bin/python3
'''routes for Review objects'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
import json


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    '''Retrieve all Review objects of a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    '''Retrieve a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''Delete a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Create a Review object'''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    elif 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data['place_id'] = place_id
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    review = Review(**data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    '''Update a Review object'''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
