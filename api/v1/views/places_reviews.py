#!/usr/bin/python3

""" Module for reviews
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def review_by_place(place_id):
    """
    Return reviews by place with the id
    """
    list_reviews = []
    place = storage.get("Place", place_id)
    if place is not None:
        for review in place.reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)
    return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>')
def reviews_by_id(review_id):
    """
    Return reviews by id
    """
    review = storage.get("Review", review_id)
    if review is not None:
        return jsonify(review.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review(review_id):
    """
    Delete a review by id
    """
    review = storage.get("Review", review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({})
    return jsonify({"error": "Not found"}), 404


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['POST'])
def create_review(place_id):
    """
    Create a new object review
    """
    if not request.get_json():
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": 'Missing name'}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": 'Missing text'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": 'Missing user_id'}), 400)
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    review = request.get_json()
    user = storage.get("User", review['user_id'])
    if user is None:
        abort(404)
    review['place_id'] = place_id
    new_review = Review(**review)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update a review by id
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    params = request.get_json()
    skip = ['id', 'user_id',  'place_id', 'created_at', 'updated_at']
    for key, value in params.items():
        if key not in skip:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())


@app_views.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404
