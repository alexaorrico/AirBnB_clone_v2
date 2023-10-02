#!/usr/bin/python3
"""
    states.py file in v1/views
"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"], strict_slashes=False)
def handle_reviews(place_id):
    """
        Method to return a JSON representation of all states
    """
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        reviews = []
        for review in place_by_id.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)

    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('text') is None:
            return jsonify({'error': 'Missing text'}), 400
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400

        user_id = post['user_id']

        user_by_id = storage.get(User, user_id)
        place_by_id = storage.get(Place, place_id)

        if not user_by_id or not place_by_id:
            abort(404)

        new_review = Review(**post)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def handle_review_by_id(review_id):
    """
        Method to return a JSON representation of a state
    """
    review_by_id = storage.get(Review, review_id)
    if review_by_id is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(review_by_id.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review_by_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_id', 'updated_at', 'user_id', 'place_id']:
                setattr(review_by_id, key, value)
        storage.save()
        return jsonify(review_by_id.to_dict()), 200
