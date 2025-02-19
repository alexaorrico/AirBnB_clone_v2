#!/usr/bin/python3
"""Handles all default RESTful API actions for Review objects"""

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False, endpoint='get_all_reviews')
def get_all_reviews_in_place(place_id):
    """Returns a JSON list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    list_of_reviews = [review.to_dict() for review in place.reviews]

    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False, endpoint='get_review')
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False, endpoint='delete_review')
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False, endpoint='create_review')
def create_review(place_id):
    """Creates a Review"""
    if storage.get(Place, place_id) is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()
    user_id = json_data.get('user_id')
    if user_id is None:
        abort(400, description='Missing user_id')

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user_data = request.get_json()
    if 'text' not in user_data:
        abort(400, description='Missing text')

    json_data['place_id'] = place_id  # adds the place_id attribute
    json_data['user_id'] = user_id  # adds the user_id attribute

    # sends complete json_data to be used to create the Review object
    new_place = Review(**json_data)

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False, endpoint='update_review')
def update_review(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()

    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200
