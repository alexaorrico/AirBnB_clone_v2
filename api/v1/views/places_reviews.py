#!/usr/bin/python3
"""
View for reviews that handles all RESTful API actions
"""
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """Returns a list of all reviews in a given place"""
    data = []
    if storage.get(Place, place_id) is None:
        abort(404)
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            data.append(review.to_dict())
    return jsonify(data)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Returns a single review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review = review.to_dict()
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """"Deletes a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """Adds a new review of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    review = review.to_dict()
    return jsonify(review), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    special_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in special_keys:
            setattr(review, key, value)
        review.save()
        review = review.to_dict()
        return jsonify(review), 200
