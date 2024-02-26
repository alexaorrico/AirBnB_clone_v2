#!/usr/bin/python3
"""
places_reviews.py
"""
from . import app_views
from flask import jsonify
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import abort, request, Response, make_response
import json


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_per_place(place_id):
    """
    Retrieves the list of all
    Review objects of a Place
    """
    if not storage.get(Place, place_id):
        abort(404)
    desired_reviews = []
    all_reviews = storage.all(Review).values()
    for review in all_reviews:
        if review.place_id == place_id:
            desired_reviews.append(review.to_dict())
    return jsonify(desired_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_review(review_id):
    """
    Retrieves a Review object
    """
    if not storage.get(Review, review_id):
        abort(404)
    return jsonify(storage.get(Review, review_id).to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_one_review(review_id):
    """
    Retrieves a Review object
    """
    if not storage.get(Review, review_id):
        abort(404)
    storage.delete(storage.get(Review, review_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    if not storage.get(Place, place_id):
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json(force=True)
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    if not storage.get(User, data['user_id']):
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json(force=True)
    for key, value in data.items():
        if key not in [
            'id',
            'user_id',
            'place_id',
            'created_at',
                'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
