#!/usr/bin/python3
"""
Methods for Review class in our API
"""
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
import json
from flask import Flask, jsonify, request, make_response, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    """Method to get all reviews by place_id"""
    place = storage.all(Place)
    reviews = storage.all(Review)
    reviews_in_place = []
    for place in place.values():
        if place.id == place_id:
            for review in reviews.values():
                if review.place_id == place_id:
                    reviews_in_place.append(review.to_dict())
            return jsonify(reviews_in_place)
    abort(404)
    return


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get a single review by id number"""
    reviews = storage.all(Review)
    for review in reviews.values():
        if review.id == review_id:
            return(jsonify(review.to_dict()))
    abort(404)
    return


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a single review"""
    reviews = storage.all(Review)

    for review in reviews.values():
        if review.id == review_id:
            review.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review"""
    payload = request.get_json(silent=True)
    places = storage.all(Place)

    if payload is None:
        abort(400, 'Not a JSON')
    elif 'user_id' not in payload:
        abort(400, 'Missing user_id')
<<<<<<< HEAD:api/v1/views/reviews.py
    elif 'user.user_id' not in payload:
        abort(404)
=======
    elif 'text' not in payload:
        abort(400, 'Missing text')
>>>>>>> 03ee046fc51fc84f789bc97c4c1833891a2c707e:api/v1/views/places_reviews.py

    for place in places.values():
        if place.id == place_id:
            payload["place_id"] = place_id
            new_review = Review(**payload)
            new_review.save()
            return(jsonify(new_review.to_dict()), 201)
    abort(404)
    return


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Method to update a review object"""
    payload = request.get_json(silent=True)
    reviews = storage.all(Review)

    if payload is None:
        abort(400, 'Not a JSON')

    for review in reviews.values():
        if review.id == review_id:
            for k, v in payload.items():
                if k != 'created_at' and k != 'updated_at' and k != 'id':
                    setattr(review, k, v)
            review.save()
            return(jsonify(review.to_dict()), 200)
    abort(404)
