#!/usr/bin/python3
"""
    Handles default RestFul API actions for place objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET', 'POST'],
    strict_slashes=False
)
def reviews_all(place_id):
    """
        Handle all objects
    """
    list_of_reviews = []
    objects = storage.all(Review).values()
    for obj in objects:
        list_of_reviews.append(obj.to_dict())

    if request.method == 'GET':
        return jsonify(list_of_reviews)

    if request.method == 'POST':
        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        if 'text' not in request_dict.keys():
            abort(400, 'Missing text')

        if 'user_id' not in request_dict.keys():
            abort(400, 'Missing user_id')

        user_obj = storage.get(User, review_obj.user_id)
        if user_obj is None:
            abort(404)

        new_review = Review(**request_dict)
        new_review.save()

        return jsonify(new_review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False
)
def reviews_by_id(review_id):
    """
        Handle objects by ID
    """

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        review_obj.delete()
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in request_dict.items():
            if key in ignore_keys:
                continue
            setattr(review_obj, key, value)
        review_obj.save()

        return jsonify(review_obj.to_dict()), 200
