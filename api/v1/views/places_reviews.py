#!/usr/bin/python3
"""
This file contains the Review module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """ Gets reviews for place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ create new instance """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)
    if 'text' not in request.get_json():
        return (jsonify({"error": "Missing text"}), 400)
    if 'user_id' not in request.get_json():
        return (jsonify({"error": "Missing user_id"}), 400)
    user_id = request.get_json().get('user_id')
    if not storage.get(User, user_id):
        abort(404)

    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates the review method"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
