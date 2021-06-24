#!/usr/bin/python3
""" Module to handle reviews RESTful API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def all_reviews(place_id):
    places = storage.all(Place).values()
    reviews = storage.all(Review).values()
    users = storage.all(User).values()

    review = [review for review in reviews if review.place_id == place_id]

    place = [place for place in places if place.id == place_id]
    if len(place) == 0:
        abort(404)

    if request.method == 'GET':
        return jsonify(list(map(lambda x: x.to_dict(), review)))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        if 'text' not in request.json:
            abort(400, 'Missing text')
        new_dict = request.get_json()
        user = [user for user in users if user.id == new_dict['user_id']]
        if len(user) == 0:
            abort(404)
        new_dict['place_id'] = place_id
        obj = Review(**new_dict)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def one_review(review_id):
    reviews = storage.all(Review).values()
    review = [review for review in reviews if review.id == review_id]
    if len(review) == 0:
        abort(404)

    if request.method == 'GET':
        return review[0].to_dict()

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.get_json().items():
            if k not in ('id', 'created_at', 'updated_at',
                         'user_id', 'place_id'):
                setattr(review[0], k, v)
        storage.save()
        return jsonify(review[0].to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(review[0])
        storage.save()
        return {}, 200
