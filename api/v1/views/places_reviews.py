#!/usr/bin/python3
"""register places in blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['GET'],
        strict_slashes=False
        )
def reviews_place(place_id=None):
    """return places of a city"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    list_reviews = []
    for review in place.reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviews(review_id=None):
    """return place by id"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def reviews_delete(review_id=None):
    """delete place by id"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'],
        strict_slashes=False
        )
def reviews_post(place_id=None):
    """add new place"""
    response = request.get_json()
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if response is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in response.keys():
        abort(400, 'Missing user_id')
    user = storage.get('User', response['user_id'])
    if user is None:
        abort(404)
    if 'text' not in response.keys():
        abort(400, 'Missing text')
    response['place_id'] = place_id
    new_review = Review(**response)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def reviews_put(review_id=None):
    """update places obj"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    response.pop('id', None)
    response.pop('user_id', None)
    response.pop('place_id', None)
    response.pop('created_at', None)
    response.pop('updated_at', None)
    for key, value in response.items():
        setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
