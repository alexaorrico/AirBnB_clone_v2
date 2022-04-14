#!/usr/bin/python3
""" API view for Review objects. """
from api.v1.views import app_views
from flask import jsonify, request, abort
import json
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

import os


@app_views.route('\
/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def all_reviews(place_id):
    """ Returns the list of reviews in Place obj in JSON. """
    review_list = []
    try:
        place = storage.all(Place)["Place.{}".format(place_id)]
    except (TypeError, KeyError):
        abort(404)
    if not place:
        abort(404)
    all_reviews = storage.all(Review)
    for review in all_reviews.values():
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ Returns the Review obj in JSON. """
    try:
        review = storage.all(Review)["Review.{}".format(review_id)]
    except (TypeError, KeyError):
        abort(404)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('\
/reviews/<review_id>', strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """ Deletes the Review obj from Storage. """
    try:
        review = storage.all(Review)["Review.{}".format(review_id)]
    except (TypeError, KeyError):
        abort(404)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('\
/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """ Creates a Review obj and saves to Storage. """
    try:
        place = storage.all(Place)["Place.{}".format(place_id)]
    except (TypeError, KeyError):
        abort(404)
    if not place:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
        if 'text' not in request.json:
            abort(400, {'message': 'Missing text'})
        if 'user_id' not in content:
            abort(400, {'message': 'Missing user_id'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    try:
        user = storage.all(User)["User.{}".format(content['user_id'])]
    except (TypeError, KeyError):
        abort(404)
    if not user:
        abort(404)
    content['place_id'] = place_id
    new_review = Review(**content)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """ Updates a Review obj to Storage. """
    if not request.json:
        abort(400, {'message': 'Not a JSON'})
    try:
        review = storage.all(Review)["Review.{}".format(review_id)]
    except (TypeError, KeyError):
        abort(404)
    if not review:
        abort(404)
    content = request.get_json()
    json.dumps(content)

    ignored_keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in content.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
