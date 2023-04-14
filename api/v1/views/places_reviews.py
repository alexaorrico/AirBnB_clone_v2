#!/usr/bin/python3
'''
    Place route for the API
'''
from flask import Flask
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_review(place_id):
    """get review information for all places"""
    reviewsList = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        reviewsList.append(review.to_dict())
    return jsonify(reviewsList)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """get review information for specific places"""
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review based on its place_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create a review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    createJson = request.get_json()
    if createJson is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'text' not in createJson.keys():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    if 'user_id' not in createJson.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    createJson['place_id'] = place_id
    place = storage.get(Place, createJson['place_id'])
    if place is None:
        abort(404)
    review = Review(**createJson)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr != 'id' or attr != 'created_at' or attr != 'updated_at' \
           or attr != 'user_id' or attr != 'place_id':
            setattr(Review, attr, val)
    storage.save()
    return jsonify(Review.to_dict())
