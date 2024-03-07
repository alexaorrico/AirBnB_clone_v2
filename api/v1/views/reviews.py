#!/usr/bin/python3
"""
View for `Review` object that handles all default RESTFul API actions.
"""
from models import storage
from flask import jsonify, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views, Review, Place


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_reviews(place_id):
    """returns: list of all reviews from specified place"""
    places = storage.all(Place)
    for place in places.values():
        if place.id == place_id:
            review_list = []
            reviews = storage.all(Review)
            for review in reviews.values():
                if review.place_id == place_id:
                    review_list.append(review)
            return review_list
    # place_id is not linked to any Place object
    abort(404)


@app_views.route("/reviews/review_id", strict_slashes=False)
def get_review(review_id):
    """returns: a specified review object"""
    reviews = storage.all(Review)
    if review in reviews.values():
        if review.id == review_id:
            return jsonify(review.to_dict())
    # object not found
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes: a review object"""
    reviews = storage.all(Review)
    for review in reviews.values():
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
    # object not found
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """creates: a review object"""
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    data_user_id = getattr(data, 'user_id')
    users = storage.all(User)
    for user in users.values():
        if user.id == data_user_id:
            places = storage.all(Review)
            for place in places.values():
                if place.id == place_id:
                    new_review = Review(**data)
                    storage.new(new_review)
                    storage.save()
                    return jsonify(new_review.to_dict()), 201
            # place_id not linked to any Place object
            abort(404)
    # user_id not linked to any User object
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """updates: a specified review object"""
    reviews = storage.all(Review)
    for review in reviews.vaalues():
        if review.id == review_id:
            try:
                data = request.get_json()
            except BadRequest:
                abort(400, 'Not a JSON')
            for k, v in data.items():
                if k == 'id' or k == 'user_id' or k == 'place_id'
                or k == 'created_at' or k == 'updated_at':
                    continue
                setattr(review, k, v)
            return jsonify(review.to_dict()), 200
    # object not found
    abort(404)
