#!/usr/bin/python3
"""A rule is being implemented that enables us to access reviews
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from models.base_model import BaseModel


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def give_all_reviews(place_id):
    """
    show us reviews partaining to a specified place
    """
    output = []
    defined_place = storage.get(Place, place_id)
    if defined_place is None:
        abort(404)
    if request.method == 'GET':
        for onePlace in defined_place.reviews:
            output.append(onePlace.to_dict())
        return (jsonify(output))
    if request.method == 'POST':
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        user_id = user_data['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if 'text' not in request.json:
            abort(400, description="Missing text")
        user_data['place_id'] = place_id
        review = Review(**user_data)
        review.save()
        return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=[
                 'GET', 'PUT', 'DELETE'], strict_slashes=False)
def give_single_review(review_id):
    """
    used to show a particular review
    according to its id
    """
    user_review = storage.get(Review, review_id)
    if user_review is None:
        abort(404)
    if request.method == 'GET':
        out_put = user_review.to_dict()
        return (jsonify(out_put))
    if request.method == 'PUT':
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in user_data.items():
            setattr(user_review, key, value)
        user_review.save()
        return (jsonify(user_review.to_dict()), 200)
    if request.method == 'DELETE':
        storage.delete(user_review)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
