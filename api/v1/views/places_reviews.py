#!/usr/bin/python3
"""This module declares city routes"""
import models
from flask import jsonify, abort
from flask import request as req
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def review_objects(place_id):
    """Returns review objects as JSON response"""
    place = models.storage.get('Place', place_id)
    if place is None:
        abort(404)

    if req.method == 'GET':
        reviews = [obj.to_dict() for obj in place.reviews]
        return jsonify(reviews)

    if req.method == 'POST':
        body = req.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if body.get('text', None) is None:
            abort(400, 'Missing text')
        if body.get('user_id', None) is None:
            abort(400, 'Missing user_id')

        user = models.storage.get('User', body.get('user_id'))
        if user is None:
            abort(404)

        review = Review(**body)
        review.place_id = place_id
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review_res(review_id):
    """Returns a Review object as JSON response"""
    review = models.storage.get('Review', review_id)
    if review is None:
        abort(404)

    if req.method == 'GET':
        return jsonify(review.to_dict())

    if req.method == 'PUT':
        review_json = req.get_json()
        if review_json is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, val in review_json.items():
            if key not in ignore:
                review.__setattr__(key, val)
        models.storage.save()
        return jsonify(review.to_dict())

    if req.method == 'DELETE':
        review.delete()
        models.storage.save()
        return jsonify({})
