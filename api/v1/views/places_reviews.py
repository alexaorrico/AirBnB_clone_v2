#!/usr/bin/python3
"""Inplementation of reviews API v1"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_all_reviews(place_id):
    """
        All review objects related to a place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews]), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review_id(review_id):
    """
        Review object based on its id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """
        Stores with id and returns a review in a given place
    """
    review_object = request.get_json(silent=True)
    if not review_object:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if 'user_id' not in review_object:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, review_object.get('user_id'))
    if not user:
        abort(404)
    if 'text' not in review_object:
        return jsonify({'error': 'Missing text'}), 400
    review_object['place_id'] = place_id
    review = Review(**review_object)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """
        Returns the data of a given review
    """
    keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review_object = request.get_json(silent=True)
    if not review_object:
        return jsonify({'error': 'Not a JSON'}), 400
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    for key, val in review_object.items():
        if key not in keys:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """
        Deletes a review with id and returns an empty JSON
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
