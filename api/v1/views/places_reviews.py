#!/usr/bin/python3
"""
handles REST API actions for State
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
    '/places/<string:place_id>/reviews',
    methods=['GET', 'POST'],
    strict_slashes=False)
def reviews(place_id):
    """handles states route"""
    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(
            [obj.to_dict() for obj in my_place.reviews])

    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None or type(post_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400

        user_id = post_data.get('user_id')
        if user_id is None:
            return jsonify({'error': 'Missing user_id'}), 400

        my_user = storage.get("User", user_id)
        if my_user is None:
            abort(404)

        text = post_data.get('text')
        if text is None:
            return jsonify({'error': 'Missing text'}), 400
        new_review = Review(place_id=place_id, **post_data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route(
    '/reviews/<string:review_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False)
def specific_review(review_id):
    """handles states route with a parameter state_id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        put_data = request.get_json()
        if put_data is None or type(put_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        to_ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        review.update(to_ignore, **put_data)
        return jsonify(review.to_dict()), 200
