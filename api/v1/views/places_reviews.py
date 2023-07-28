#!/usr/bin/python3
"""Creatte the review function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
import models


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    """retrieves all reviews linked to a place"""
    state = models.storage.get("Place", place_id)
    if state:
        city = models.storage.all("Review")
        all_city = []
        for ct in city.values():
            if ct.place_id == place_id:
                all_city.append(ct.to_dict())
        return jsonify(all_city)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_a_review_with_id(review_id):
    """get a review using id"""
    answer = models.storage.get("Review", review_id)
    if answer:
        return jsonify(answer.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_a_review_with_id(review_id):
    """delete a review using id"""
    answer = models.storage.get("Review", review_id)
    if answer:
        answer.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_a_review_router(place_id):
    """create a review"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in request.json:
        return jsonify({"error": "Missing text"}), 400
    status = models.storage.get("Place", place_id)
    if status is None:
        abort(404)
    userid = request.get_json().get('user_id')
    stat = models.storage.get("User", userid)
    if stat is None:
        abort(404)
    values = request.get_json()
    new_state = Review(**values)
    new_state.place_id = place_id
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_a_review_with_id(review_id):
    """update a review using id"""
    answer = models.storage.get("Review", review_id)
    if answer:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in request.get_json().items():
            if k not in ['id', 'user_id',
                         'created_at', 'updated_at', 'state_id']:
                setattr(answer, k, v)
        answer.save()
        return jsonify(answer.to_dict()), 200
    abort(404)
