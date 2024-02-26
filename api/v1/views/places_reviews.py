#!/usr/bin/python3
"""
Module for handling Review objects API endpoints
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_reviews(place_id):
    """Handles GET and POST requests for /places/<place_id>/reviews endpoint"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')

        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        user_id = data['user_id']
        user = storage.get(User, user_id)

        if user is None:
            abort(404)

        if 'text' not in data:
            abort(400, 'Missing text')

        new_review = Review(place_id=place_id, user_id=user_id, **data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review(review_id):
    """Handles GET, DELETE, and PUT requests for /reviews/<review_id> endpoint"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review, key, value)

        review.save()
        return jsonify(review.to_dict()), 200

