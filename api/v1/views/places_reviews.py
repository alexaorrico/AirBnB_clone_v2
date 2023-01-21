#!/usr/bin/python3
"""reviews"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from models.base_model import BaseModel


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    """list all reviews in place"""
    output = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        for onePlace in place.reviews:
            output.append(onePlace.to_dict())
        return (jsonify(output))
    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        user_id = data['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if 'text' not in request.json:
            abort(400, description="Missing text")
        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=[
                 'GET', 'PUT', 'DELETE'], strict_slashes=False)
def a_review(review_id):
    """list a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        output = review.to_dict()
        return (jsonify(output))
    if request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(review, key, value)
        review.save()
        return (jsonify(review.to_dict()), 200)
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
