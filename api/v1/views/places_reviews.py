#!/usr/bin/python3
"""states script"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def list_all_reviews(place_id):
    '''Retrieves a list of all review objects of a state id'''
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object by ID"""
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object by ID"""
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_id = request_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if 'text' not in request_data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    request_data['place_id'] = place_id
    new_review = Review(**request_data)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
