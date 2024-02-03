#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from flask import abort, jsonify, request
import json


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    review_list = []
    review_dict = storage.all(Review)
    for review in review_dict.values():
        if place_id == review.place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_id(review_id):
    review = storage.get(Place, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    review = storage.get(Place, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify('{}'), 201


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def places_review_post(place_id):
    try:
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        data_object['place_id'] = place_id
        if 'user_id' not in data_object:
            abort(400, 'Missing user_id')
        if 'text' not in data_object:
            abort(400, 'Missing text')
        user = storage.get(User, data_object['user_id'])
        if not user:
            abort(404)
        new_place_review = Review(**data_object)
        storage.new(new_place_review)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(new_place_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_put(review_id):
    try:
        review_up = storage.get(Review, review_id)
        if not review_up:
            abort(404)
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        for key, value in data_object.items():
            setattr(review_up, key, value)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(review_up.to_dict()), 201
