#!/usr/bin/python3

'''
This module creates a new view for places_reviews
Routes:
    GET /api/v1/places/<place_id>/reviews - Retrieves all review objects
    GET /api/v1/reviews/<review_id> - Retrieves a review object
    DELETE /api/v1/reviews/<review_id> - Deletes a review object
    POST /api/v1/places/<place_id>/reviews - Creates a review
    PUT /api/v1/reviews/<review_id> - Updates a review object
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    '''
    Retrieves all review objects
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    '''
    Retrieves a review object
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''
    Deletes a review object
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
    Creates a new review
    '''
    place = storage.get(Place, place_id)
    body = request.get_json()
    if place is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in body:
        abort(400, 'Missing user_id')
    if 'text' not in body:
        abort(400, 'Missing text')
    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    body['place_id'] = place_id
    review = Review(**body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    '''
    Updates a review object
    '''
    review = storage.get(Review, review_id)
    body = request.get_json()
    if review is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    for k, v in body.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
