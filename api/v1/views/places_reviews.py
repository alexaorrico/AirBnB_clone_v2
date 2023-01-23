#!/usr/bin/python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from models.base_model import BaseModel


@app_views.route('/places/<place_id>/reviews',
                 methods=["GET", "POST"], strict_slashes=False)
def get_reviews(place_id):
    """get all instances of reviews in a place"""
    response = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        for review in place.reviews:
            response.append(review.to_dict())
        return (jsonify(response))

    if request.method == "POST":
        """post a new instance"""
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        user_id = new_data['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if 'name' not in request.json:
            abort(400, description="Missing name")
        new_data['place_id'] = place_id
        review = Review(**new_data)
        review.save()
        return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """get, update an instance of review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        response = review.to_dict()
        return (jsonify(response))
    if request.method == "PUT":
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in new_data.items():
            setattr(review, key, value)
        review.save()
        return (jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """delete an instance of review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        response = make_response(jsonify({}), 200)
        return response
