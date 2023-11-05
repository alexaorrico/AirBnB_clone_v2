#!/usr/bin/python3
'''places.py'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id=None):
    '''get reviwes by place'''
    place = storage.get(Place, place_id)
    if place:
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    '''get review'''
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
        else:
            abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    '''delete review'''
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    '''post review'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    if 'text' not in request.get_json():
        return jsonify({'error': 'Missing text'}), 400
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    place = storage.get(Place, place_id)
    if place:
        review = Review(**request.get_json())
        review.place_id = place.id
        review.save()
        return jsonify(review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    '''UPdate review'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    review = storage.get(Review, review_id)
    if review:
        (request.get_json()).pop('id', None)
        (request.get_json()).pop('updated_at', None)
        (request.get_json()).pop('created_at', None)
        (request.get_json()).pop('place_id', None)
        (request.get_json()).pop('user_id', None)
        for key, value in request.get_json().items():
            setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
    else:
        abort(404)
