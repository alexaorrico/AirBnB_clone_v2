#!/usr/bin/python3
'''BLueprint implementation for review model'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
import os


@app_views.route('reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_reviews(review_id=None):
    '''Return the list of all Review objects'''
    if request.method == 'DELETE':
        return del_review(review_id)
    elif request.method == 'PUT':
        return update_review(review_id)
    elif request.method == 'GET':
        return get_reviews(review_id)


@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_place_reviews(place_id):
    '''Hadnles direction to actual view function'''
    if request.method == 'POST':
        return add_review(place_id)
    elif request.method == 'GET':
        return get_place_reviews(place_id)


def get_place_reviews(place_id):
    '''Return all citie linked to a place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        reviews = place.reviews()
    else:
        reviews = list(place.reviews)
    return jsonify([review.to_dict() for review in reviews])


def get_reviews(review_id):
    '''Reurn a review given an id'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


def del_review(review_id):
    '''Deletes a review obj with place_id'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


def add_review(place_id):
    '''Adds review to reviews'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    if 'text' not in req_data:
        abort(400, 'Missing text')
    if 'user_id' not in req_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, req_data['user_id'])
    if not user:
        abort(404)
    review = Review(**req_data)
    review.place_id = place.id
    review.save()
    return get_reviews(review.id), 201


def update_review(review_id):
    '''Update a review instance'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    skip = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    for key, val in req_data.items():
        if key not in skip:
            setattr(review, key, val)
    review.save()
    return get_reviews(review.id), 200
