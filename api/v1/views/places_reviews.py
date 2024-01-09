#!/usr/bin/python3
"""Module for handling places reviews in the API"""

# Import statements
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Get reviews for a specified place"""
    place_instance = storage.get("Place", place_id)
    if place_instance is None:
        abort(404)
    reviews_list = []
    for review_instance in place_instance.reviews:
        reviews_list.append(review_instance.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get review information for specified review"""
    review_instance = storage.get("Review", review_id)
    if review_instance is None:
        abort(404)
    return jsonify(review_instance.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review based on its review_id"""
    review_instance = storage.get("Review", review_id)
    if review_instance is None:
        abort(404)
    review_instance.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Create a new review"""
    place_instance = storage.get("Place", place_id)
    if place_instance is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_instance = storage.get("User", kwargs['user_id'])
    if user_instance is None:
        abort(404)
    if 'text' not in kwargs:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    kwargs['place_id'] = place_id
    new_review = Review(**kwargs)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Update a review"""
    review_instance = storage.get("Review", review_id)
    if review_instance is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(review_instance, attr, val)
    review_instance.save()
    return jsonify(review_instance.to_dict())
