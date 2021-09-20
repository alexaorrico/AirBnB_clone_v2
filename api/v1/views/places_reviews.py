#!/usr/bin/python3
"""
User for API.
"""
from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
    'places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False)
def get_id_places_r(places_id):
    """Returns id places in json format"""
    place_id = storage.get(Place, places_id)
    if place_id:
        reviews = []
        for review in place_id.reviews:
            reviews.append(review.to_dict())
        return (jsonify(reviews), 200)
    abort(404)


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False)
def get_review(review_id):
    """Returns JSON review"""
    review = storage.get('Review', review_id)
    if review:
        return (jsonify(review.to_dict()), 200)
    abort(404)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_review(review_id):
    """Deletes review"""
    review = storage.get(Eeview, review_id)
    if review:
        review.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route(
    '/reviews/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False)
def post_review(place_id):
    """Creates review"""
    all_review = request.get_json()
    place = storage.get('Place', place_id)
    if not all_review:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'text' not in all_review:
        return (jsonify({'error': 'Missing text'}), 400)
    if 'user_id' not in all_review:
        return (jsonify({'error': 'Missing user_id'}), 400)
    if storage.get('User', request.get_json()['user_id']) and place:
        review = Review(**all_review)
        review.place_id = place_id
        review.save()
        return (jsonify(review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_review(review_id):
    """Updates a review """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key in data.keys():
        if key not in ignore:
            setattr(review, key, data[key])
