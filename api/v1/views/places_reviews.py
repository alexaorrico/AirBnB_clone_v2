#!/usr/bin/python3
"""
a view for City objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'])
def get_add_reviews(place_id):
    """
    get review information for a place otherwise 404
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        kwargs = request.get_json()
        if 'user_id' not in kwargs:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        user = storage.get("User", kwargs['user_id'])
        if user is None:
            abort(404)
        if 'text' not in kwargs:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        kwargs['place_id'] = place_id
        review = Review(**kwargs)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)



@app_views.route('/reviews/<string:review_id>', methods=['GET', 'DELETE', 'PUT'])
def manageReviews(review_id):
    """
    manipulate review information for specified place
    """
    reviewObj = storage.get("Review", review_id)
    if reviewObj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(reviewObj.to_dict())

    if request.method == 'DELETE':
        reviewObj.delete()
        storage.save()
        return (jsonify({}))

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review, attr, val)
        place.save()
        return jsonify(review.to_dict())
