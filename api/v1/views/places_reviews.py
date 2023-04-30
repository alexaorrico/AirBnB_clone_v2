#!/usr/bin/python3
'''
places_reviews handler
'''
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_by_place(place_id):
    """reviews by place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([review.to_dict()
                        for review in place.reviews])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
        if 'text' not in request.get_json():
            abort(400, 'Missing text')
        if not storage.get('User', request.get_json()['user_id']):
            abort(404)
        new_Review = Review(**request.get_json())
        new_Review.place_id = place_id
        new_Review.save()
        return jsonify(new_Review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review(review_id):

    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ["id", "user_id", "place_id",
                           "created_at", "updated_at"]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
