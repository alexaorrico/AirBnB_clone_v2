#!/usr/bin/python3
"""
This module defines API endpoints for handling Review objects related
to Place objects. It provides functionalities for CRUD operations
following RESTful API principles.
"""

from flask import Blueprint, jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

bp = Blueprint('places_reviews', __name__)


@bp.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects for a specified Place.
    If the place_id is not linked to any Place object, a 404 error is raised.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: List of Review objects in JSON format.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@bp.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object by its ID.
    If the review_id is not linked to any Review object, a 404 error is raised.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON: The Review object in JSON format.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@bp.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object by its ID.
    If the review_id is not linked to any Review object, a 404 error is raised.
    Returns an empty dictionary with status code 200.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON: An empty dictionary with status code 200.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@bp.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Creates a new Review object for a specified Place.
    If the place_id is not linked to any Place object, a 404 error is raised.
    If the HTTP body request is not valid JSON, a 400 error with the message
    "Not a JSON" is raised.
    If the dictionary doesn’t contain the key user_id, a 400 error with the
    message "Missing user_id" is raised.
    If the user_id is not linked to any User object, a 404 error is raised.
    If the dictionary doesn’t contain the key text, a 400 error with the
    message "Missing text" is raised.
    Returns the new Review with the status code 201.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: The new Review object in JSON format with status code 201.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@bp.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object by its ID.
    If the review_id is not linked to any Review object, a 404 error is raised.
    If the HTTP request body is not valid JSON, a 400 error with the message
    "Not a JSON" is raised.
    Updates the Review object with all key-value pairs of the dictionary,
    ignoring keys: id, user_id, place_id, created_at, and updated_at.
    Returns the updated Review object with the status code 200.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON: The updated Review object in JSON format with status code 200.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    ignore_keys = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
