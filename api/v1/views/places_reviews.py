#!/usr/bin/python3

"""
A view for Place objects that handles all default RESTFul API Actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def reviews_by_place(place_id):
    """Retrieves and posts reviews by place_id."""
    # Retrieve the Place object with the given place_id
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # Action for GET method
    if request.method == 'GET':
        review_list = [review.to_dict() for review in place.reviews]
        return jsonify(review_list)

    # Action for POST method
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    # Check if the user with the specified user_id exists
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    new_review = Review(place_id=place_id, **data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):
    """Retrieves, deletes, or updates a review by id."""
    # Retrieve the Review object with the given review_id
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    # Action for GET method
    if request.method == 'GET':
        return jsonify(review.to_dict())

    # Action for DELETE method
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    # Action for PUT method
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        # Save updated Review object
        storage.save()
        return jsonify(review.to_dict()), 200
