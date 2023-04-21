#!/usr/bin/python3
"""Handles RESTful API actions for Review objects."""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieve list of all Review objects for a specific Place object."""
    place = None  # Replace with code to get Place object by place_id
    if place is None:
        abort(404)
    reviews = []  # Replace with code to get list of Review objects for the given Place object
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a specific Review object by ID."""
    review = None  # Replace with code to get Review object by review_id
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a specific Review object by ID."""
    review = None  # Replace with code to get Review object by review_id
    if review is None:
        abort(404)
    # Replace with code to delete the Review object
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new Review object for a specific Place object."""
    place = None  # Replace with code to get Place object by place_id
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = None  # Replace with code to get User object by user_id
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    # Replace with code to create a new Review object using the provided data
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a specific Review object by ID."""
    review = None  # Replace with code to get Review object by review_id
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    # Replace with code to update the Review object using the provided data
    return jsonify(review.to_dict()), 200
