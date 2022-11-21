#!/usr/bin/python3
"""
    Handles API functions for Review
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_review(place_id):
    """
        Retrieves reviews of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    if request.method == 'POST':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        if 'user_id' not in info:
            abort(400, 'Missing user_id')
        user = storage.get(User, info['user_id'])
        if user is None:
            abort(404)
        if 'text' not in info:
            abort(400, 'Missing text')
        info['place_id'] = place_id
        new_review = Review(**info)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_review(review_id):
    """
        Handles a specific review
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        for key, value in info.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id',
                       'place_id']:
                pass
            else:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
