#!/usr/bin/python3
"""
Module for Place object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """ Retrieves the list of all reviews of a place """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        reviews_list = []
        for review in place_obj.reviews:
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ Retrieves the dict of a Review object """
    try:
        review_dic = storage.get(Review, review_id).to_dict()
        return jsonify(review_dic)
    except:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Delete a Review object """
    review_obj = storage.get(Review, review_id)
    if review_obj is not None:
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ Create a new Review object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'text' not in request.json:
        return make_response(jsonify({"error": "Missing text"}), 400)

    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    data = request.get_json()
    user_id = data['user_id']
    place_obj = storage.get(Place, place_id)
    user_obj = storage.get(User, user_id)
    if place_obj and user_obj:
        data['place_id'] = place_id
        new_review = Review(**data)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ Update a Review object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    try:
        review_obj = storage.get(Review, review_id)
        data = request.get_json()

        for key, value in data.items():
            if key != 'updated_at' or key != 'created_at':
                if key != 'id' or key != 'place_id' or key != 'user_id':
                    setattr(review_obj, key, value)

        storage.save()
        return jsonify(review_obj.to_dict()), 200
    except:
        abort(404)
