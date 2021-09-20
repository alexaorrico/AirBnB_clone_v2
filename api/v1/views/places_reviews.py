#!/usr/bin/python3
"""
Review view for API.
"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False)
def get_review_by_place(place_id):
    """Returns JSON reviews"""
    place = storage.get('Place', place_id)
    if place:
        list_review = []
        for review in place.list_review:
            list_review.append(review.to_dict())
        return (jsonify(list_review), 200)
    abort(404)


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False)
def get_review(review_id):
    """Returns JSON review id"""
    review = storage.get('Review', review_id)
    if review:
        return (jsonify(review.to_dict()), 200)
    abort(404)


@app_views.route(
    '/reviews/<review_id>',
    methods=['Delete'],
    strict_slashes=False)
def delete_review(review_id):
    """Deletes review"""
    review = storage.get('Review', review_id)
    if review:
        review.delete()
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route(
    '/reviews/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False)
def post_review(place_id):
    """Creates review """
    reviews = request.get_json()
    place = storage.get('Place', place_id)
    if not reviews:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'text' not in reviews:
        return (jsonify({'error': 'Missing text'}))
    elif 'user_id' not in reviews:
        return (jsonify({'error': 'Missing user_id'}), 400)
    elif storage.get('User', request.get_json()['user_id']) and place:
        review = Review(**reviews)
        review.place_id = place_id
        review.save()
        return (jsonify(review.to_dict()), 201)
    abort(404)


@app_views.route(
    '/reviews/<review_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_review(review_id):
    """Updates review"""
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    reviews = request.get_json()
    review = storage.get('Review', review_id)
    if not reviews:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if review:
        for key in reviews.keys():
            if key not in ignore:
                setattr(review, key, reviews[key])
    abort(404)
