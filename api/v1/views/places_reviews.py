#!/usr/bin/python3
"""
Module that houses the view for Review objects
It handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_review_list(place_id):
    """Retrieves the list of all Review objects"""
    reviews_list = []
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list), 200


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review_obj(review_id):
    """
    Retrieves an Review object

    Args:
        review_id: The id of the review object
    Raises:
        404: if review_id supplied is not linked to any amenity object
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews_obj(review_id):
    """
    Deletes an Review object

    Args:
        review_id: The id of the review object
    Raises:
        404: if review_id supplied is not linked to any amenity object
    """
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates an Review object

    Returns:
        The new Review with the status code 201
    """
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, data["user_id"])
    if not user:
        return jsonify({'error': 'Not found'}), 404
    if 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400
    data["place_id"] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates an Review object

    Args:
        review_id: The id of the review object
    Raises:
        404:
            If review_id supplied is not linked to any review o    bject
            400: If the HTTP body request is not valid JSON
    """
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
