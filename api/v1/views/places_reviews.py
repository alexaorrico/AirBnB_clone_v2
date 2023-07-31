#!/usr/bin/python3
'''
Module: 'places_reviews'
'''

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['GET'],
        strict_slashes=False
        )
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    return jsonify([review.to_dict() for review in Place.get(
        place_id).reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    return jsonify(Review.get(review_id).to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_review(review_id):
    """ Deletes a Review object """
    Review.get(review_id).delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'],
        strict_slashes=False
        )
def create_review(place_id):
    """ Creates a Review """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'text' not in request.json:
        abort(400, 'Missing text')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    review = Review(**request.json)
    setattr(review, 'place_id', place.id)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at'
                ]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
