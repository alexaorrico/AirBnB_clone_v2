#!/usr/bin/python3
"""
Handle all default RESTFUL API actions
"""
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_reviews(place_id):
    """ Returns infor for reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        u_id = storage.get(User, data.get('user_id'))
        if u_id is None:
            abort(404)
        if 'text' not in data:
            abort(400, 'Missing text')
        new_review = Review(**data)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def review(review_id):
    """ Returns review object of id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            ign_attr = ['id', 'created_at', 'updated_at']
            if k not in ign_attr:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200

    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
