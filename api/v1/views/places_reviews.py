#!/usr/bin/python3
"""Module to create a new view for Review objects"""

from flask import jsonify, Flask, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """Retrieves the list of all Review objs of a Place by place_id"""
    review = storage.get('Review', str(place_id))
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_review_id(review_id):
    """Retrieves a Review object by review_id"""
    review = storage.get('Review', str(review_id))
    if review is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """Deletes a review by ID"""
    review = storage.get('Review', str(review_id))
    if review is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Post a Review object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'name' not in data:
        abort(400)
        abort(Response("Missing name"))
    new_review = Review(**data)
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Put a Review object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 200
