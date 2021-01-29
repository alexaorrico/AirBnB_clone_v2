#!/usr/bin/python3
"""Modules that handles all Restful API actions for Places"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all Review objects"""
    reviews_all = storage.get('Place', place_id)
    if reviews_all is None:
        abort(404)
    list_reviews = []
    for review in reviews_all.reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def obj_review(review_id):
    """Retrieves a Review object"""
    rev = storage.get('Review', review_id)
    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a given object review"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review object"""
    new_review = storage.get('Place', place_id)
    if new_review is None:
        abort(404)
    dict_review = request.get_json()
    if not dict_review:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'text' not in dict_review:
        return jsonify({'error': 'Missing text'}), 400
    if 'user_id' not in dict_review:
        return jsonify({'error': 'Missing user_id'}), 400
    else:
        user_id = dict_review['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)

    obj = Review(**dict_review)
    setattr(obj, 'place_id', place_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        setattr(review, key, val)
    storage.save()
    return jsonify(review.to_dict()), 200
