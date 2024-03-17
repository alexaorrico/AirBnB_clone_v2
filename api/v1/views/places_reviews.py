#!/usr/bin/python3
""" API views for Review objects
Allows routes to list, get, delete, create, and update Reviews
as requested. """

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Returns the list of all review objects of the specified Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Returns a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review for a specific place"""
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, review_data['user_id'])
    if not user:
        abort(404)
    if 'text' not in review_data:
        abort(400, description="Missing text")
    review = Review(**review_data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review"""
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, description="Not a JSON")
    for key, value in review_data.items():
        if key not in [
            'id', 'user_id', 'place_id',
                'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
